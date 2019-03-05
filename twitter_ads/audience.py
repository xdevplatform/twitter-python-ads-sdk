# Copyright (C) 2015 Twitter, Inc.

"""Container for all audience management logic used by the Ads API SDK."""

from twitter_ads.enum import TRANSFORM
from twitter_ads.resource import resource_property, Resource
from twitter_ads.http import Request
from twitter_ads.error import BadRequest
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION

import json


class TailoredAudience(Resource):

    PROPERTIES = {}
    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/tailored_audiences'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/tailored_audiences/{id}'
    RESOURCE_USERS = '/' + API_VERSION + '/accounts/{account_id}/tailored_audiences/\
{id}/users'
    RESOURCE_PERMISSIONS = '/' + API_VERSION + '/accounts/{account_id}/tailored_audiences/\
{id}/permissions'

    @classmethod
    def create(klass, account, name):
        """
        Creates a new tailored audience.
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
            tailored_audience_id.
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
        Deletes the current tailored audience instance.
        """
        resource = self.RESOURCE.format(account_id=self.account.id, id=self.id)
        response = Request(self.account.client, 'delete', resource).perform()
        return self.from_response(response.body['data'])

    def permissions(self, **kwargs):
        """
        Returns a collection of permissions for the curent tailored audience.
        """
        self._validate_loaded()
        return TailoredAudiencePermission.all(self.account, self.id, **kwargs)

    def __create_audience__(self, name):
        params = {'name': name}
        resource = self.RESOURCE_COLLECTION.format(account_id=self.account.id)
        response = Request(self.account.client, 'post', resource, params=params).perform()
        return self.from_response(response.body['data'])


# tailored audience properties
# read-only
resource_property(TailoredAudience, 'id', readonly=True)
resource_property(TailoredAudience, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(TailoredAudience, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(TailoredAudience, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(TailoredAudience, 'audience_size', readonly=True)
resource_property(TailoredAudience, 'audience_type', readonly=True)
resource_property(TailoredAudience, 'metadata', readonly=True)
resource_property(TailoredAudience, 'partner_source', readonly=True)
resource_property(TailoredAudience, 'reasons_not_targetable', readonly=True)
resource_property(TailoredAudience, 'targetable', readonly=True)
resource_property(TailoredAudience, 'targetable_types', readonly=True)
# writable
resource_property(TailoredAudience, 'name')
resource_property(TailoredAudience, 'list_type')


class TailoredAudiencePermission(Resource):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/tailored_audiences/'
    RESOURCE_COLLECTION += '{tailored_audience_id}/permissions'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/tailored_audiences/\
{tailored_audience_id}/permissions/{id}'

    @classmethod
    def all(klass, account, tailored_audience_id, **kwargs):
        """Returns a Cursor instance for the given tailored audience permission resource."""

        resource = klass.RESOURCE_COLLECTION.format(
            account_id=account.id,
            tailored_audience_id=tailored_audience_id)
        request = Request(account.client, 'get', resource, params=kwargs)

        return Cursor(klass, request, init_with=[account])

    def save(self):
        """
        Saves or updates the current tailored audience permission.
        """
        if self.id:
            method = 'put'
            resource = self.RESOURCE.format(
                account_id=self.account.id,
                tailored_audience_id=self.tailored_audience_id,
                id=self.id)
        else:
            method = 'post'
            resource = self.RESOURCE_COLLECTION.format(
                account_id=self.account.id,
                tailored_audience_id=self.tailored_audience_id)

        response = Request(
            self.account.client, method,
            resource, params=self.to_params()).perform()

        return self.from_response(response.body['data'])

    def delete(self):
        """
        Deletes the current tailored audience permission.
        """
        resource = self.RESOURCE.format(
            account_id=self.account.id,
            tailored_audience_id=self.tailored_audience_id,
            id=self.id)
        response = Request(self.account.client, 'delete', resource).perform()
        return self.from_response(response.body['data'])


# tailored audience permission properties
# read-only
resource_property(TailoredAudiencePermission, 'id', readonly=True)
resource_property(TailoredAudiencePermission, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(TailoredAudiencePermission, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(TailoredAudiencePermission, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(TailoredAudiencePermission, 'tailored_audience_id')
resource_property(TailoredAudiencePermission, 'granted_account_id')
resource_property(TailoredAudiencePermission, 'permission_level')


class AudienceIntelligence(Resource):

    PROPERTIES = {}

    RESOURCE_BASE = '/' + API_VERSION + '/accounts/{account_id}/audience_intelligence/'
    RESOURCE_CONVERSATIONS = RESOURCE_BASE + 'conversations'
    RESOURCE_DEMOGRAPHICS = RESOURCE_BASE + 'demographics'
    METHOD = 'post'
    HEADERS = {'Content-Type': 'application/json'}

    @classmethod
    def __get(klass, account, client, params):
        """
        Helper function to get the conversation data
        Returns a Cursor instance
        """
        resource = klass.RESOURCE_CONVERSATIONS.format(account_id=account.id)

        request = Request(
            account.client, klass.METHOD,
            resource, headers=klass.HEADERS, body=params)
        return Cursor(klass, request, init_with=[account])

    def conversations(self):
        """
        Get the conversation topics for an input targeting criteria
        """
        body = {
            "conversation_type": self.conversation_type,
            "audience_definition": self.audience_definition,
            "targeting_inputs": self.targeting_inputs
        }
        return self.__get(account=self.account, client=self.account.client, params=json.dumps(body))

    def demographics(self):
        """
        Get the demographic breakdown for an input targeting criteria
        """
        body = {
            "audience_definition": self.audience_definition,
            "targeting_inputs": self.targeting_inputs
        }
        resource = self.RESOURCE_DEMOGRAPHICS.format(account_id=self.account.id)
        response = Request(
            self.account.client, self.METHOD,
            resource, headers=self.HEADERS, body=json.dumps(body)).perform()
        return response.body['data']


# tailored audience permission properties
# read-only
resource_property(AudienceIntelligence, 'operator_type', readonly=True)
resource_property(AudienceIntelligence, 'targeting_type', readonly=True)
resource_property(AudienceIntelligence, 'targeting_value', readonly=True)
resource_property(AudienceIntelligence, 'localized', readonly=True)
# writable
resource_property(AudienceIntelligence, 'conversation_type')
resource_property(AudienceIntelligence, 'targeting_inputs')
resource_property(AudienceIntelligence, 'audience_definition')
# demographics only
resource_property(AudienceIntelligence, 'start_time', transform=TRANSFORM.TIME)
resource_property(AudienceIntelligence, 'end_time', transform=TRANSFORM.TIME)
