# Copyright (C) 2015 Twitter, Inc.

"""Container for all HTTP request and response logic for the SDK."""

import sys
import platform
import datetime
import logging
import httplib

from dateutil import parser
from requests_oauthlib import OAuth1Session

from twitter_ads.utils import get_version
from twitter_ads.error import Error


class Request(object):
    """Generic container for all API requests."""

    _DEFAULT_DOMAIN = 'https://ads-api.twitter.com'
    _SANDBOX_DOMAIN = 'https://ads-api-sandbox.twitter.com'

    def __init__(self, client, method, resource, **kwargs):
        self._client = client
        self._method = method.lower()
        self._resource = resource
        self._options = kwargs.copy()

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

        consumer = OAuth1Session(
            self._client.consumer_key,
            client_secret=self._client.consumer_secret,
            resource_owner_key=self._client.access_token,
            resource_owner_secret=self._client.access_token_secret)

        url = self.__domain() + self._resource
        method = getattr(consumer, self._method)
        response = method(url, headers=headers, data=data, params=params)

        return Response(response.status_code, response.headers,
                        body=response.json(), raw_body=response.text)

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
        self._body = kwargs.get('body', None) or self._raw_body

        if 'x-rate-limit-reset' in headers:
            self._rate_limit = int(headers['x-rate-limit-limit'])
            self._rate_limit_remaining = int(headers['x-rate-limit-remaining'])
            self._rate_limit_reset = datetime.datetime.fromtimestamp(
                int(headers['x-rate-limit-reset']))
        elif 'x-cost-rate-limit-reset' in headers:
            self._rate_limit = int(headers['x-cost-rate-limit-limit'])
            self._rate_limit_remaining = int(
                headers['x-cost-rate-limit-remaining'])
            self._rate_limit_reset = parser.parse(
                headers['x-cost-rate-limit-reset'].first)
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
