# Copyright (C) 2015 Twitter, Inc.

"""
A Twitter supported and maintained Ads API SDK for Python.
"""

from twitter_ads.enum import TRANSFORM
from twitter_ads.http import Request
from twitter_ads.cursor import Cursor

from twitter_ads.resource import resource_property, Resource
from twitter_ads.creative import AccountMedia, MediaCreative, Video
from twitter_ads.audience import TailoredAudience
from twitter_ads.campaign import (FundingInstrument, Campaign, LineItem,
                                  AppList, PromotableUser)


class Account(Resource):
    """
    The Ads API :class:`Account` class which functions as a context container
    for the advertiser and nearly all interactions with the API.
    """

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/1/accounts'
    RESOURCE = '/1/accounts/{id}'
    FEATURES = '/1/accounts/{id}/features'
    SCOPED_TIMELINE = '/1/accounts/{id}/scoped_timeline'

    def __init__(self, client):
        self._client = client

    @property
    def client(self):
        return self._client

    @property
    def account(self):
        return NotImplementedError

    @classmethod
    def load(klass, client, id, **kwargs):
        """Returns an object instance for a given resource."""
        resource = klass.RESOURCE.format(id=id)
        response = Request(client, 'get', resource, params=kwargs).perform()
        return klass(client).from_response(response.body['data'])

    @classmethod
    def all(klass, client, **kwargs):
        """Returns a Cursor instance for a given resource."""
        resource = klass.RESOURCE_COLLECTION
        request = Request(client, 'get', resource, params=kwargs)
        return Cursor(klass, request, init_with=[client])

    def reload(self, **kwargs):
        """
        Reloads all attributes for the current object instance from the API.
        """
        if not self.id:
            return self

        params = {'with_deleted': True}
        params.update(kwargs)

        resource = self.RESOURCE.format(account_id=self.account.id, id=self.id)
        response = Request(self.account.client, 'get', resource, params=params).perform()

        self.from_response(response.body['data'])

    def features(self):
        """
        Returns a collection of features available to the current account.
        """
        self._validate_loaded()

        resource = self.FEATURES.format(id=self.id)
        response = Request(self.client, 'get', resource).perform()

        return response.body['data']

    def promotable_users(self, id=None, **kwargs):
        """
        Returns a collection of promotable users available to the
        current account.
        """
        return self._load_resource(PromotableUser, id, **kwargs)

    def funding_instruments(self, id=None, **kwargs):
        """
        Returns a collection of funding instruments available to
        the current account.
        """
        return self._load_resource(FundingInstrument, id, **kwargs)

    def campaigns(self, id=None, **kwargs):
        """
        Returns a collection of campaigns available to the current account.
        """
        return self._load_resource(Campaign, id, **kwargs)

    def line_items(self, id=None, **kwargs):
        """
        Returns a collection of line items available to the current account.
        """
        return self._load_resource(LineItem, id, **kwargs)

    def app_lists(self, id=None, **kwargs):
        """
        Returns a collection of app lists available to the current account.
        """
        return self._load_resource(AppList, id, **kwargs)

    def tailored_audiences(self, id=None, **kwargs):
        """
        Returns a collection of tailored audiences available to the
        current account.
        """
        return self._load_resource(TailoredAudience, id, **kwargs)

    def videos(self, id=None, **kwargs):
        """
        Returns a collection of videos available to the current account.
        """
        return self._load_resource(Video, id, **kwargs)

    def account_media(self, id=None, **kwargs):
        """
        Returns a collection of account media available to the current account.
        """
        return self._load_resource(AccountMedia, id, **kwargs)

    def media_creatives(self, id=None, **kwargs):
        """
        Returns a collection of media creatives available to the current account.
        """
        return self._load_resource(MediaCreative, id, **kwargs)

    def scoped_timeline(self, *id, **kwargs):
        """
        Returns the most recent promotable Tweets created by the specified Twitter user.
        """
        self._validate_loaded()

        params = {'user_id': id}
        params.update(kwargs)

        resource = self.SCOPED_TIMELINE.format(id=self.id)
        response = Request(self.client, 'get', resource, params=params).perform()

        return response.body['data']

# account properties
resource_property(Account, 'id', readonly=True)
resource_property(Account, 'name', readonly=True)
resource_property(Account, 'salt', readonly=True)
resource_property(Account, 'timezone', readonly=True)
resource_property(Account, 'approval_status', readonly=True)
resource_property(Account, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(Account, 'timezone_switch_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(Account, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(Account, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
