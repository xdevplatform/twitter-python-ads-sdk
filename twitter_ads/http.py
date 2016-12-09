# Copyright (C) 2015 Twitter, Inc.

"""Container for all HTTP request and response logic for the SDK."""

import os
import sys
import platform
import logging
import json
import zlib

try:
    import httplib2 as httplib
except ImportError:
    if sys.version_info[0] != 3:
        import httplib
    else:
        import http.client as httplib

import dateutil.parser
from datetime import datetime, timedelta

from requests_oauthlib import OAuth1Session

from twitter_ads.utils import get_version, http_time
from twitter_ads.error import Error


class Request(object):
    """Generic container for all API requests."""

    _DEFAULT_DOMAIN = 'https://ads-api.twitter.com'
    _SANDBOX_DOMAIN = 'https://ads-api-sandbox.twitter.com'

    _HTTP_METHOD = [
        'get',
        'put',
        'post',
        'delete',
    ]

    def __init__(self, client, method, resource, **kwargs):
        self._client = client
        self._resource = resource
        self._options = kwargs.copy()

        method = method.lower()
        if method not in self._HTTP_METHOD:
            msg = "Error! {0} is not an allowed HTTP method type.".format(method)
            raise ValueError(msg)

        self._method = method

    @property
    def options(self):
        return self._options

    @property
    def client(self):
        return self._client

    @property
    def method(self):
        return self._method

    @property
    def resource(self):
        return self._resource

    def perform(self):
        if self.client.trace:
            self.__enable_logging()
        response = self.__oauth_request()
        if response.code > 399:
            raise Error.from_response(response)
        return response

    def __oauth_request(self):
        headers = {'user-agent': self.__user_agent()}
        if 'headers' in self.options:
            headers.update(self.options['headers'].copy())

        params = self.options.get('params', None)
        data = self.options.get('body', None)
        files = self.options.get('files', None)
        stream = self.options.get('stream', False)

        consumer = OAuth1Session(
            self._client.consumer_key,
            client_secret=self._client.consumer_secret,
            resource_owner_key=self._client.access_token,
            resource_owner_secret=self._client.access_token_secret)

        url = self.__domain() + self._resource
        method = getattr(consumer, self._method)

        response = method(url, headers=headers, data=data, params=params,
                          files=files, stream=stream)

        raw_response_body = response.raw.read() if stream else response.text

        return Response(response.status_code, response.headers,
                        body=response.raw, raw_body=raw_response_body)

    def __enable_logging(self):
        httplib.HTTPConnection.debuglevel = 1
        logging.basicConfig(level=logging.DEBUG)
        logging.propagate = True

    def __user_agent(self):
        python_verison = "{0}.{1}".format(sys.version_info.major, sys.version_info.minor)
        return 'twitter-ads version: {0} platform: Python {1} ({2}/{3})'.format(
            get_version(),
            python_verison,
            platform.python_implementation(),
            sys.platform)

    def __domain(self):
        if self.client.sandbox:
            return self._SANDBOX_DOMAIN
        return self.options.get('domain', self._DEFAULT_DOMAIN)


class Response(object):
    """Generic container for API responses."""

    def __init__(self, code, headers, **kwargs):
        self._code = code
        self._headers = headers
        self._raw_body = kwargs.get('raw_body', None)

        if headers.get('content-type') == 'application/gzip':
            # hack because Twitter TON API doesn't return headers as it should
            # and instead returns a gzipp'd file rather than a gzipp encoded response
            # Content-Encoding: gzip
            # Content-Type: application/json
            # instead it returns:
            # Content-Type: application/gzip
            raw_response_body = zlib.decompress(self._raw_body, 16 + zlib.MAX_WBITS).decode()
        else:
            raw_response_body = self._raw_body

        try:
            self._body = json.loads(raw_response_body)
        except ValueError:
            self._body = raw_response_body

        if 'x-rate-limit-reset' in headers:
            self._rate_limit = int(headers['x-rate-limit-limit'])
            self._rate_limit_remaining = int(headers['x-rate-limit-remaining'])
            self._rate_limit_reset = datetime.fromtimestamp(int(headers['x-rate-limit-reset']))
        elif 'x-cost-rate-limit-reset' in headers:
            self._rate_limit = int(headers['x-cost-rate-limit-limit'])
            self._rate_limit_remaining = int(headers['x-cost-rate-limit-remaining'])
            self._rate_limit_reset = dateutil.parser.parse(headers['x-cost-rate-limit-reset'].first)
        else:
            self._rate_limit = None
            self._rate_limit_remaining = None
            self._rate_limit_reset = None

    @property
    def code(self):
        return self._code

    @property
    def headers(self):
        return self._headers

    @property
    def body(self):
        return self._body

    @property
    def raw_body(self):
        return self._raw_body

    @property
    def rate_limit(self):
        return self._rate_limit

    @property
    def rate_limit_remaining(self):
        return self._rate_limit_remaining

    @property
    def rate_limit_reset(self):
        return self._rate_limit_reset

    @property
    def error(self):
        return True if (self._code >= 400 and self._code <= 599) else False


class TONUpload(object):
    """Specialized request class for TON API uploads."""

    _DEFAULT_DOMAIN = 'https://ton.twitter.com'
    _DEFAULT_RESOURCE = '/1.1/ton/bucket/'
    _DEFAULT_BUCKET = 'ta_partner'
    _DEFAULT_EXPIRE = datetime.now() + timedelta(days=10)
    _MIN_FILE_SIZE = 1024 * 1024 * 1

    def __init__(self, client, file_path, **kwargs):
        if not os.path.isfile(file_path):
            msg = "Error! The specified file does not exist. ({0})".format(file_path)
            raise ValueError(msg)

        self._file_path = os.path.abspath(file_path)
        self._file_size = os.path.getsize(self._file_path)
        self._client = client
        self._options = kwargs.copy()
        self._bucket = self._options.pop('bucket', self._DEFAULT_BUCKET)

    @property
    def options(self):
        return self._options

    @property
    def client(self):
        return self._client

    @property
    def bucket(self):
        return self._bucket

    @property
    def content_type(self):
        """Returns the content-type value determined by file extension."""

        if hasattr(self, '_content_type'):
            return self._content_type

        filename, extension = os.path.splitext(self._file_path)
        if extension == '.csv':
            self._content_type = 'text/csv'
        elif extension == '.tsv':
            self._content_type = 'text/tab-separated-values'
        else:
            self._content_type = 'text/plain'

        return self._content_type

    def perform(self):
        """Executes the current TONUpload object."""

        if self._file_size < self._MIN_FILE_SIZE:
            resource = "{0}{1}".format(self._DEFAULT_RESOURCE, self.bucket)
            response = self.__upload(resource, open(self._file_path, 'rb').read())
            return response.headers['location']
        else:
            response = self.__init_chunked_upload()
            chunk_size = int(response.headers['x-ton-min-chunk-size'])
            location = response.headers['location']

            f = open(self._file_path, 'rb')
            bytes_read = 0
            while True:
                bytes = f.read(chunk_size)
                if not bytes:
                    break
                bytes_start = bytes_read
                bytes_read += len(bytes)
                self.__upload_chunk(location, chunk_size, bytes, bytes_start, bytes_read)
            f.close()

            return location

    def __repr__(self):
        return '<{name} object at {mem} bucket={bucket} file={file}>'.format(
            name=self.__class__.__name__,
            mem=hex(id(self)),
            bucket=self.bucket,
            file=self._file_path
        )

    def __upload(self, resource, bytes):
        """Performs a single chunk upload."""

        # note: string conversion required here due to open encoding bug in requests-oauthlib.
        headers = {
            'x-ton-expires': http_time(self.options.get('x-ton-expires', self._DEFAULT_EXPIRE)),
            'content-length': str(self._file_size),
            'content-type': self.content_type
        }

        return Request(self._client, 'post', resource,
                       domain=self._DEFAULT_DOMAIN, headers=headers, body=bytes).perform()

    def __init_chunked_upload(self):
        """Initialization for a multi-chunk upload."""

        # note: string conversion required here due to open encoding bug in requests-oauthlib.
        headers = {
            'x-ton-content-type': self.content_type,
            'x-ton-content-length': str(self._file_size),
            'x-ton-expires': http_time(self.options.get('x-ton-expires', self._DEFAULT_EXPIRE)),
            'content-length': str(0),
            'content-type': self.content_type
        }

        resource = "{0}{1}?resumable=true".format(self._DEFAULT_RESOURCE, self._DEFAULT_BUCKET)

        return Request(self._client, 'post', resource,
                       domain=self._DEFAULT_DOMAIN, headers=headers).perform()

    def __upload_chunk(self, resource, chunk_size, bytes, bytes_start, bytes_read):
        """Uploads a single chunk of a multi-chunk upload."""

        # note: string conversion required here due to open encoding bug in requests-oauthlib.
        headers = {
            'content-type': self.content_type,
            'content-length': str(min([chunk_size, self._file_size - bytes_read])),
            'content-range': "bytes {0}-{1}/{2}".format(
                bytes_start, bytes_read - 1, self._file_size)
        }

        return Request(self._client, 'put', resource,
                       domain=self._DEFAULT_DOMAIN, headers=headers, body=bytes).perform()
