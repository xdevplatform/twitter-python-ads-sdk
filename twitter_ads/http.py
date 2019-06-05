# Copyright (C) 2015 Twitter, Inc.

"""Container for all HTTP request and response logic for the SDK."""

import sys
import platform
import logging
import json
import zlib

if sys.version_info[0] != 3:
    import httplib
else:
    import http.client as httplib

import dateutil.parser
from datetime import datetime
from requests_oauthlib import OAuth1Session
from twitter_ads.utils import get_version
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
            raw_response_body = zlib.decompress(self._raw_body, 16 + zlib.MAX_WBITS).decode('utf-8')
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
