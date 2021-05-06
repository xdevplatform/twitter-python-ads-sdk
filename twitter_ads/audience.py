# Copyright (C) 2015 Twitter, Inc.

"""Container for all audience management logic used by the Ads API SDK."""

from twitter_ads.enum import TRANSFORM
from twitter_ads.resource import resource_property, Resource
from twitter_ads.http import Request
from twitter_ads.error import BadRequest
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION

import json


class CustomAudience(Resource):

    PROPERTIES = {}
    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/custom_audiences'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/custom_audiences/{id}'
    RESOURCE_USERS = '/' + API_VERSION + '/accounts/{account_id}/custom_audiences/\
{id}/users'
    RESOURCE_PERMISSIONS = '/' + API_VERSION + '/accounts/{account_id}/custom_audiences/\
{id}/permissions'

    @classmethod
    def create(klass, account, name):
        """
        Creates a new custom audience.
        """
        audience = klass(account)
        getattr(audience, '__create_audience__')(name)
        try:
            return audience.reload()
        except BadRequest as e:
            audience.delete()
            raise e

    def users(self, params):
        """
        This is a private API and requires whitelisting from Twitter.
        This endpoint will allow partners to add, update and remove users from a given
        custom_audience_id.
        The endpoint will also accept multiple user identifier types per user as well.
        """
        resource = self.RESOURCE_USERS.format(account_id=self.account.id, id=self.id)
        headers = {'Content-Type': 'application/json'}
        response = Request(self.account.client,
                           'post',
                           resource,
                           headers=headers,
                           body=json.dumps(params)).perform()
        success_count = response.body['data']['success_count']
        total_count = response.body['data']['total_count']
        return (success_count, total_count)

    def delete(self):
        """
        Deletes the current custom audience instance.
        """
        resource = self.RESOURCE.format(account_id=self.account.id, id=self.id)
        response = Request(self.account.client, 'delete', resource).perform()
        return self.from_response(response.body['data'])

    def permissions(self, **kwargs):
        """
        Returns a collection of permissions for the curent custom audience.
        """
        self._validate_loaded()
        return CustomAudiencePermission.all(self.account, self.id, **kwargs)

    def targeted(self, **kwargs):
        """
        Returns a collection of campaigns and line items targeting the curent custom audience.
        """
        self._validate_loaded()
        return CustomAudienceTargeted.all(self.account, self.id, **kwargs)

    def __create_audience__(self, name):
        params = {'name': name}
        resource = self.RESOURCE_COLLECTION.format(account_id=self.account.id)
        response = Request(self.account.client, 'post', resource, params=params).perform()
        return self.from_response(response.body['data'])


# Custom audience properties
# read-only
resource_property(CustomAudience, 'id', readonly=True)
resource_property(CustomAudience, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(CustomAudience, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(CustomAudience, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(CustomAudience, 'audience_size', readonly=True)
resource_property(CustomAudience, 'audience_type', readonly=True)
resource_property(CustomAudience, 'partner_source', readonly=True)
resource_property(CustomAudience, 'reasons_not_targetable', readonly=True)
resource_property(CustomAudience, 'targetable', readonly=True)
resource_property(CustomAudience, 'targetable_types', readonly=True)
resource_property(CustomAudience, 'owner_account_id', readonly=True)

# writable
resource_property(CustomAudience, 'name')
resource_property(CustomAudience, 'description')


class CustomAudiencePermission(Resource):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/custom_audiences/'
    RESOURCE_COLLECTION += '{custom_audience_id}/permissions'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/custom_audiences/\
{custom_audience_id}/permissions/{id}'

    @classmethod
    def all(klass, account, custom_audience_id, **kwargs):
        """Returns a Cursor instance for the given custom audience permission resource."""

        resource = klass.RESOURCE_COLLECTION.format(
            account_id=account.id,
            custom_audience_id=custom_audience_id)
        request = Request(account.client, 'get', resource, params=kwargs)

        return Cursor(klass, request, init_with=[account])

    def save(self):
        """
        Saves or updates the current custom audience permission.
        """
        resource = self.RESOURCE_COLLECTION.format(
            account_id=self.account.id,
            custom_audience_id=self.custom_audience_id)

        response = Request(
            self.account.client, 'post',
            resource, params=self.to_params()).perform()

        return self.from_response(response.body['data'])

    def delete(self):
        """
        Deletes the current custom audience permission.
        """
        resource = self.RESOURCE.format(
            account_id=self.account.id,
            custom_audience_id=self.custom_audience_id,
            id=self.id)
        response = Request(self.account.client, 'delete', resource).perform()
        return self.from_response(response.body['data'])


# custom audience permission properties
# read-only
resource_property(CustomAudiencePermission, 'id', readonly=True)
resource_property(CustomAudiencePermission, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(CustomAudiencePermission, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(CustomAudiencePermission, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(CustomAudiencePermission, 'custom_audience_id')
resource_property(CustomAudiencePermission, 'granted_account_id')
resource_property(CustomAudiencePermission, 'permission_level')


class CustomAudienceTargeted(Resource):

    PROPERTIES = {}

    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/custom_audiences/\
{custom_audience_id}/targeted'

    @classmethod
    def all(klass, account, custom_audience_id, **kwargs):
        """Returns a Cursor instance for the given targeted custom audience resource."""

        resource = klass.RESOURCE.format(
            account_id=account.id,
            custom_audience_id=custom_audience_id)
        request = Request(account.client, 'get', resource, params=kwargs)

        return Cursor(klass, request, init_with=[account])


# custom audience targeted properties
# read-only
resource_property(CustomAudienceTargeted, 'campaign_id', readonly=True)
resource_property(CustomAudienceTargeted, 'campaign_name', readonly=True)
resource_property(CustomAudienceTargeted, 'line_items', readonly=True)
resource_property(CustomAudienceTargeted, 'id', readonly=True)
resource_property(CustomAudienceTargeted, 'name', readonly=True)
resource_property(CustomAudienceTargeted, 'servable', readonly=True, transform=TRANSFORM.BOOL)

# writable
resource_property(CustomAudienceTargeted, 'custom_audience_id')
resource_property(CustomAudienceTargeted, 'with_active', transform=TRANSFORM.BOOL)
