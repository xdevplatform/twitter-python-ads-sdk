# Copyright (C) 2015 Twitter, Inc.

"""Container for all Cursor logic used by the Ads API SDK."""

# from twitter_ads import *
from twitter_ads.http import Request


class Cursor(object):
    """
    The Ads API Client class which functions as a container for basic
    API consumer information.
    """

    def __init__(self, klass, request, **kwargs):
        self._klass = klass
        self._client = request.client
        self._method = request.method
        self._resource = request.resource

        self._options = kwargs.copy()
        self._options.update(request.options)

        self._collection = []
        self._current_index = 0
        self._next_cursor = None
        self._total_count = 0

        self.__from_response(request.perform())

    @property
    def exhausted(self):
        """
        Returns True if the custor instance is exhausted.
        """
        return False if self._next_cursor else True

    @property
    def count(self):
        """
        Returns the total number of items available to this cursor instance.
        """
        return self._total_count or len(self._collection)

    @property
    def first(self):
        """
        Returns the first item of available items available to the cursor instance.
        """
        return next(iter(self._collection), None)

    @property
    def fetched(self):
        """
        Returns the number of items fetched so far.
        """
        return len(self._collection)

    def __iter__(self):
        return self

    def next(self):
        """Returns the next item in the cursor."""
        if self._current_index < len(self._collection):
            value = self._collection[self._current_index]
            self._current_index += 1
            return value
        elif self._next_cursor:
            self.__fetch_next()
            return self.next()
        else:
            self._current_index = 0
            raise StopIteration

    __next__ = next

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__die()

    def __fetch_next(self):
        options = self._options.copy()
        params = options.get('params', {})
        params.update({'cursor': self._next_cursor})
        options['params'] = params
        response = Request(self._client, self._method, self._resource, **options).perform()
        return self.__from_response(response)

    def __from_response(self, response):
        self._next_cursor = response.body.get('next_cursor', None)
        if 'total_count' in response.body:
            self._total_count = int(response.body['total_count'])

        for item in response.body['data']:
            if 'from_response' in dir(self._klass):
                init_with = self._options.get('init_with', None)
                obj = self._klass(*init_with) if init_with else self._klass()
                self._collection.append(obj.from_response(item))
            else:
                self._collection.append(item)
