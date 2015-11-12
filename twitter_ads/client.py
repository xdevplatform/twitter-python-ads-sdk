# Copyright (C) 2015 Twitter, Inc.

"""
A Twitter supported and maintained Ads API SDK for Python.
"""

from twitter_ads.account import Account


class Client(object):
    """
    The Ads API Client class which functions as a container for basic
    API consumer information.
    """

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token,
                 access_token_secret,
                 **kwargs):
        """
        Creates a new Ads API client instance.

        ..seealso:: :doc:`/examples/quick_start.py`
        """
        self._consumer_key = consumer_key
        self._consumer_secret = consumer_secret
        self._access_token = access_token
        self._access_token_secret = access_token_secret
        self._options = kwargs

    def __repr__(self):
        return '<{name} object at {mem} consumer_key={key}>'.format(
            name=self.__class__.__name__,
            mem=hex(id(self)),
            key=getattr(self, 'consumer_key')
        )

    @property
    def consumer_key(self):
        """Returns the consumer_key value."""
        return self._consumer_key

    @property
    def consumer_secret(self):
        """Returns the consumer_secret value."""
        return self._consumer_secret

    @property
    def access_token(self):
        """Returns the access_token value."""
        return self._access_token

    @property
    def access_token_secret(self):
        """Returns the access_token_secret value."""
        return self._access_token_secret

    def sandbox():
        """Enables and disables sandbox mode."""
        def fget(self):
            return self._options.get('sandbox', None)

        def fset(self, value):
            self._options['sandbox'] = value

        return locals()

    sandbox = property(**sandbox())

    def trace():
        """Enables and disables request tracing."""
        def fget(self):
            return self._options.get('trace', None)

        def fset(self, value):
            self._options['trace'] = value

        return locals()

    trace = property(**trace())

    def accounts(self, id=None):
        """
        Returns a collection of advertiser :class:`Accounts` available to
        the current access token.
        """
        return Account.load(self, id) if id else Account.all(self)
