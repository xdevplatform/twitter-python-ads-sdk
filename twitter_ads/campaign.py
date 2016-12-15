# Copyright (C) 2015 Twitter, Inc.

"""Container for all campaign management logic used by the Ads API SDK."""

from twitter_ads.enum import TRANSFORM
from twitter_ads.resource import resource_property, Resource, Persistence, Batch, Analytics
from twitter_ads.http import Request
from twitter_ads.cursor import Cursor


class TargetingCriteria(Resource, Persistence, Batch):

    PROPERTIES = {}

    BATCH_RESOURCE_COLLECTION = '/1/batch/accounts/{account_id}/targeting_criteria'
    RESOURCE_COLLECTION = '/1/accounts/{account_id}/targeting_criteria'
    RESOURCE = '/1/accounts/{account_id}/targeting_criteria/{id}'

    @classmethod
    def all(klass, account, line_item_id, **kwargs):
        """Returns a Cursor instance for a given resource."""
        params = {'line_item_id': line_item_id}
        params.update(kwargs)

        resource = klass.RESOURCE_COLLECTION.format(account_id=account.id)
        request = Request(account.client, 'get', resource, params=params)

        return Cursor(klass, request, init_with=[account])

# targeting criteria properties
# read-only
resource_property(TargetingCriteria, 'id', readonly=True)
resource_property(TargetingCriteria, 'localized_name', readonly=True)
resource_property(TargetingCriteria, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(TargetingCriteria, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(TargetingCriteria, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(TargetingCriteria, 'line_item_id')
resource_property(TargetingCriteria, 'operator_type')
resource_property(TargetingCriteria, 'targeting_type')
resource_property(TargetingCriteria, 'targeting_value')
resource_property(TargetingCriteria, 'tailored_audience_expansion')
resource_property(TargetingCriteria, 'tailored_audience_type')
# sdk-only
resource_property(TargetingCriteria, 'to_delete', transform=TRANSFORM.BOOL)


class FundingInstrument(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/1/accounts/{account_id}/funding_instruments'
    RESOURCE = '/1/accounts/{account_id}/funding_instruments/{id}'

# funding instrument properties
# read-only
resource_property(FundingInstrument, 'id', readonly=True)
resource_property(FundingInstrument, 'name', readonly=True)
resource_property(FundingInstrument, 'cancelled', readonly=True, transform=TRANSFORM.BOOL)
resource_property(FundingInstrument, 'credit_limit_local_micro', readonly=True)
resource_property(FundingInstrument, 'currency', readonly=True)
resource_property(FundingInstrument, 'description', readonly=True)
resource_property(FundingInstrument, 'funded_amount_local_micro', readonly=True)
resource_property(FundingInstrument, 'type', readonly=True)
resource_property(FundingInstrument, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(FundingInstrument, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(FundingInstrument, 'deleted', readonly=True, transform=TRANSFORM.BOOL)


class PromotableUser(Resource):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/1/accounts/{account_id}/promotable_users'
    RESOURCE = '/1/accounts/{account_id}/promotable_users/{id}'

# promotable user properties
# read-only
resource_property(PromotableUser, 'id', readonly=True)
resource_property(PromotableUser, 'promotable_user_type', readonly=True)
resource_property(PromotableUser, 'user_id', readonly=True)
resource_property(PromotableUser, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(PromotableUser, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(PromotableUser, 'deleted', readonly=True, transform=TRANSFORM.BOOL)


class AppList(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/1/accounts/{account_id}/app_lists'
    RESOURCE = '/1/accounts/{account_id}/app_lists/{id}'

    def create(self, name, *ids):
        if isinstance(ids, list):
            ids = ','.join(map(str, ids))

        resource = self.RESOURCE_COLLECTION.format(account_id=self.account.id)
        params = self.to_params.update({'app_store_identifiers': ids, 'name': name})
        response = Request(self.account.client, 'post', resource, params=params).perform()

        return self.from_response(response.body['data'])

    def apps(self):
        if self.id and not hasattr(self, '_apps'):
            self.reload()
        return self._apps

# app list properties
# read-only
resource_property(AppList, 'id', readonly=True)
resource_property(AppList, 'name', readonly=True)
resource_property(AppList, 'apps', readonly=True)


class Campaign(Resource, Persistence, Analytics, Batch):

    PROPERTIES = {}

    BATCH_RESOURCE_COLLECTION = '/1/batch/accounts/{account_id}/campaigns'
    RESOURCE_COLLECTION = '/1/accounts/{account_id}/campaigns'
    RESOURCE = '/1/accounts/{account_id}/campaigns/{id}'

# campaign properties
# read-only
resource_property(Campaign, 'id', readonly=True)
resource_property(Campaign, 'reasons_not_servable', readonly=True)
resource_property(Campaign, 'servable', readonly=True, transform=TRANSFORM.BOOL)
resource_property(Campaign, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(Campaign, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(Campaign, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(Campaign, 'name')
resource_property(Campaign, 'funding_instrument_id')
resource_property(Campaign, 'start_time', transform=TRANSFORM.TIME)
resource_property(Campaign, 'end_time', transform=TRANSFORM.TIME)
resource_property(Campaign, 'paused', transform=TRANSFORM.BOOL)
resource_property(Campaign, 'currency')
resource_property(Campaign, 'standard_delivery')
resource_property(Campaign, 'daily_budget_amount_local_micro')
resource_property(Campaign, 'total_budget_amount_local_micro')
# sdk-only
resource_property(Campaign, 'to_delete', transform=TRANSFORM.BOOL)


class LineItem(Resource, Persistence, Analytics, Batch):

    PROPERTIES = {}

    BATCH_RESOURCE_COLLECTION = '/1/batch/accounts/{account_id}/line_items'
    RESOURCE_COLLECTION = '/1/accounts/{account_id}/line_items'
    RESOURCE = '/1/accounts/{account_id}/line_items/{id}'

    def targeting_criteria(self, id=None, **kwargs):
        """
        Returns a collection of targeting criteria available to the
        current line item.
        """
        self._validate_loaded()
        if id is None:
            return TargetingCriteria.all(self.account, self.id, **kwargs)
        else:
            return TargetingCriteria.load(self.account, id, **kwargs)

# line item properties
# read-only
resource_property(LineItem, 'id', readonly=True)
resource_property(LineItem, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(LineItem, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(LineItem, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(LineItem, 'name')
resource_property(LineItem, 'campaign_id')
resource_property(LineItem, 'advertiser_domain')
resource_property(LineItem, 'categories', transform=TRANSFORM.LIST)
resource_property(LineItem, 'charge_by')
resource_property(LineItem, 'include_sentiment')
resource_property(LineItem, 'objective')
resource_property(LineItem, 'optimization')
resource_property(LineItem, 'paused', transform=TRANSFORM.BOOL)
resource_property(LineItem, 'primary_web_event_tag')
resource_property(LineItem, 'product_type')
resource_property(LineItem, 'placements', transform=TRANSFORM.LIST)
resource_property(LineItem, 'bid_unit')
resource_property(LineItem, 'automatically_select_bid', transform=TRANSFORM.BOOL)
resource_property(LineItem, 'bid_amount_local_micro')
resource_property(LineItem, 'total_budget_amount_local_micro')
resource_property(LineItem, 'bid_type')
# sdk-only
resource_property(LineItem, 'to_delete', transform=TRANSFORM.BOOL)


class Tweet(object):

    TWEET_PREVIEW = '/1/accounts/{account_id}/tweet/preview'
    TWEET_ID_PREVIEW = '/1/accounts/{account_id}/tweet/preview/{id}'
    TWEET_CREATE = '/1/accounts/{account_id}/tweet'

    def __init__(self):
        raise NotImplementedError(
            'Error! {name} cannot be instantiated.'.format(name=self.__class__.__name__))

    @classmethod
    def preview(klass, account, **kwargs):
        """
        Returns an HTML preview of a tweet, either new or existing.
        """
        params = {}
        params.update(kwargs)

        # handles array to string conversion for media IDs
        if 'media_ids' in params and isinstance(params['media_ids'], list):
            params['media_ids'] = ','.join(map(params['media_ids']))

        resource = klass.TWEET_ID_PREVIEW if params.get('id') else klass.TWEET_PREVIEW
        resource = resource.format(account_id=account.id, id=params.get('id'))
        response = Request(account.client, 'get', resource, params=params).perform()
        return response.body['data']

    @classmethod
    def create(klass, account, status, **kwargs):
        """
        Creates a "Promoted-Only" Tweet using the specialized Ads API end point.
        """
        params = {'status': status}
        params.update(kwargs)

        # handles array to string conversion for media IDs
        if 'media_ids' in params and isinstance(params['media_ids'], list):
            params['media_ids'] = ','.join(map(params['media_ids']))

        resource = klass.TWEET_CREATE.format(account_id=account.id)
        response = Request(account.client, 'post', resource, params=params).perform()
        return response.body['data']
