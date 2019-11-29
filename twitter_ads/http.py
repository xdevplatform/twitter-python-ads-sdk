# Copyright (C) 2015 Twitter, Inc.

"""Container for all HTTP request and response logic for the SDK."""

import sys
import platform
import logging
logger = logging.getLogger(__name__)
import json
import zlib
import time

if sys.version_info[0] != 3:
    import httplib
else:
    import http.client as httplib

from requests.exceptions import Timeout
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

        # internal-only
        if 'x-as-user' in self._client.options:
            headers['x-as-user'] = self._client.options.get('x-as-user')

        params = self.options.get('params', None)
        data = self.options.get('body', None)
        files = self.options.get('files', None)
        stream = self.options.get('stream', False)

        handle_rate_limit = self._client.options.get('handle_rate_limit', False)
        retry_max = self._client.options.get('retry_max', 0)
        retry_delay = self._client.options.get('retry_delay', 1500)
        retry_on_status = self._client.options.get('retry_on_status', [500, 503])
        retry_on_timeouts = self._client.options.get('retry_on_timeouts', False)
        timeout = self._client.options.get('timeout', None)
        retry_count = 0
        retry_after = None
        timeout = self._client.options.get('timeout', None)

        consumer = OAuth1Session(
            self._client.consumer_key,
            client_secret=self._client.consumer_secret,
            resource_owner_key=self._client.access_token,
            resource_owner_secret=self._client.access_token_secret)

        url = self.__domain() + self._resource
        method = getattr(consumer, self._method)

        while (retry_count <= retry_max):
            try:
                response = method(url, headers=headers, data=data, params=params,
                                  files=files, stream=stream, timeout=timeout)
            except Timeout as e:
                if retry_on_timeouts:
                    if retry_count == retry_max:
                        raise Exception(e)
                    logger.warning("Timeout occurred: resume in %s seconds"
                                   % (int(retry_delay) / 1000))
                    time.sleep(int(retry_delay) / 1000)
                    retry_count += 1
                    continue
                raise Exception(e)

            # do not retry on 2XX status code
            if 200 <= response.status_code < 300:
                break

            if handle_rate_limit and retry_after is None:
                rate_limit_reset = response.headers.get('x-account-rate-limit-reset') \
                    or response.headers.get('x-rate-limit-reset')

                if response.status_code == 429:
                    retry_after = int(rate_limit_reset) - int(time.time())
                    logger.warning("Request reached Rate Limit: resume in %d seconds"
                                   % retry_after)
                    time.sleep(retry_after + 5)
                    continue

            if retry_max > 0:
                if response.status_code not in retry_on_status:
                    break
                time.sleep(int(retry_delay) / 1000)

            retry_count += 1

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
            # Async analytics data arrives as a gzipped file so decompress it on-the-fly.
            # Note: might need to consider using zlib.decompressobj() instead
            # in case data streams gets large enough (data size doesn't fit into memory at once)
            raw_response_body = zlib.decompress(self._raw_body, 16 + zlib.MAX_WBITS).decode('utf-8')
        else:
            raw_response_body = self._raw_body

        try:
            self._body = json.loads(raw_response_body)
        except ValueError:
            self._body = raw_response_body

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
    def error(self):
        return True if (self._code >= 400 and self._code <= 599) else False
