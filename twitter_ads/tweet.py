# Copyright (C) 2015 Twitter, Inc.

"""Container for all Tweet-related logic used by the Ads API SDK."""

from twitter_ads.resource import resource, Resource
from twitter_ads.http import Request


@resource
class Tweet(Resource):

    PROPERTIES = {
        'platform': {'readonly': True},
        'preview': {'readonly': True}
    }

    TWEET_PREVIEW = '/0/accounts/{account_id}/tweet/preview'
    TWEET_EXISTS_PREVIEW = '/0/accounts/{account_id}/tweet/preview/{tweet_id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account

    def get_preview(self, id=None, **kwargs):
        """
        Returns an HTML preview of a tweet, either new or existing.
        """
        if id is not None:
            resource = self.TWEET_EXISTS_PREVIEW.format(
                account_id=self.account.id, tweet_id=id)
        else:
            resource = self.TWEET_PREVIEW.format(
                account_id=self.account.id)

        response = Request(
            self._account.client(), 'get', resource, params=kwargs).perform()

        return response.body['data']
