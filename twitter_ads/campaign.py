# Copyright (C) 2015 Twitter, Inc.

"""Container for all campaign management logic used by the Ads API SDK."""

from twitter_ads.enum import TRANSFORM
from twitter_ads.analytics import Analytics
from twitter_ads.resource import resource_property, Resource, Persistence, Batch
from twitter_ads.http import Request
from twitter_ads.cursor import Cursor
from twitter_ads.utils import FlattenParams
from twitter_ads import API_VERSION


class TargetingCriteria(Resource, Persistence, Batch):

    PROPERTIES = {}

    BATCH_RESOURCE_COLLECTION = '/' + API_VERSION + '/batch/accounts/{account_id}/\
targeting_criteria'
    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/targeting_criteria'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/targeting_criteria/{id}'
    RESOURCE_OPTIONS = '/' + API_VERSION + '/targeting_criteria/'

    @classmethod
    @FlattenParams
    def all(klass, account, **kwargs):
        """Returns a Cursor instance for a given resource."""
        resource = klass.RESOURCE_COLLECTION.format(account_id=account.id)
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(klass, request, init_with=[account])

    @classmethod
    def app_store_categories(klass, account, **kwargs):
        """Returns a list of supported app store categories"""
        resource = klass.RESOURCE_OPTIONS + 'app_store_categories'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def behavior_taxonomies(klass, account, **kwargs):
        """Returns a list of supported behavior taxonomies"""
        resource = klass.RESOURCE_OPTIONS + 'behavior_taxonomies'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def behaviors(klass, account, **kwargs):
        """Returns a list of supported behaviors"""
        resource = klass.RESOURCE_OPTIONS + 'behaviors'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def conversations(klass, account, **kwargs):
        """Returns a list of supported conversations"""
        resource = klass.RESOURCE_OPTIONS + 'conversations'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def devices(klass, account, **kwargs):
        """Returns a list of supported devices"""
        resource = klass.RESOURCE_OPTIONS + 'devices'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def events(klass, account, **kwargs):
        """Returns a list of supported events"""
        resource = klass.RESOURCE_OPTIONS + 'events'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def interests(klass, account, **kwargs):
        """Returns a list of supported interests"""
        resource = klass.RESOURCE_OPTIONS + 'interests'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def languages(klass, account, **kwargs):
        """Returns a list of supported languages"""
        resource = klass.RESOURCE_OPTIONS + 'languages'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def locations(klass, account, **kwargs):
        """Returns a list of supported locations"""
        resource = klass.RESOURCE_OPTIONS + 'locations'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def network_operators(klass, account, **kwargs):
        """Returns a list of supported network operators"""
        resource = klass.RESOURCE_OPTIONS + 'network_operators'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def platforms(klass, account, **kwargs):
        """Returns a list of supported platforms"""
        resource = klass.RESOURCE_OPTIONS + 'platforms'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def platform_versions(klass, account, **kwargs):
        """Returns a list of supported platform versions"""
        resource = klass.RESOURCE_OPTIONS + 'platform_versions'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def tv_markets(klass, account, **kwargs):
        """Returns a list of supported TV markets"""
        resource = klass.RESOURCE_OPTIONS + 'tv_markets'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)

    @classmethod
    def tv_shows(klass, account, **kwargs):
        """Returns a list of supported TV shows"""
        resource = klass.RESOURCE_OPTIONS + 'tv_shows'
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(None, request)


# targeting criteria properties
# read-only
resource_property(TargetingCriteria, 'id', readonly=True)
resource_property(TargetingCriteria, 'name', readonly=True)
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
# sdk-only
resource_property(TargetingCriteria, 'to_delete', transform=TRANSFORM.BOOL)


class FundingInstrument(Analytics, Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/funding_instruments'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/funding_instruments/{id}'


# funding instrument properties
# read-only
resource_property(FundingInstrument, 'id', readonly=True)
resource_property(FundingInstrument, 'name', readonly=True)
resource_property(FundingInstrument, 'credit_limit_local_micro', readonly=True)
resource_property(FundingInstrument, 'currency', readonly=True)
resource_property(FundingInstrument, 'description', readonly=True)
resource_property(FundingInstrument, 'funded_amount_local_micro', readonly=True)
resource_property(FundingInstrument, 'type', readonly=True)
resource_property(FundingInstrument, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(FundingInstrument, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(FundingInstrument, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(FundingInstrument, 'able_to_fund', readonly=True, transform=TRANSFORM.BOOL)
resource_property(FundingInstrument, 'entity_status', readonly=True)
resource_property(FundingInstrument, 'io_header', readonly=True)
resource_property(FundingInstrument, 'reasons_not_able_to_fund', readonly=True,
                  transform=TRANSFORM.LIST)
resource_property(FundingInstrument, 'start_time', readonly=True)
resource_property(FundingInstrument, 'end_time', readonly=True)
resource_property(FundingInstrument, 'credit_remaining_local_micro', readonly=True)


class PromotableUser(Resource):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/promotable_users'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/promotable_users/{id}'


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

    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/app_lists'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/app_lists/{id}'

    def apps(self):
        if self.id and not hasattr(self, '_apps'):
            self.reload()
        return self._apps


# app list properties
# read-only
resource_property(AppList, 'id', readonly=True)
resource_property(AppList, 'name', readonly=True)
resource_property(AppList, 'apps', readonly=True)


class Campaign(Analytics, Resource, Persistence, Batch):

    PROPERTIES = {}

    BATCH_RESOURCE_COLLECTION = '/' + API_VERSION + '/batch/accounts/{account_id}/campaigns'
    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/campaigns'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/campaigns/{id}'


# campaign properties
# read-only
resource_property(Campaign, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(Campaign, 'currency', readonly=True)
resource_property(Campaign, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(Campaign, 'id', readonly=True)
resource_property(Campaign, 'reasons_not_servable', readonly=True)
resource_property(Campaign, 'servable', readonly=True, transform=TRANSFORM.BOOL)
resource_property(Campaign, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
# writable
resource_property(Campaign, 'daily_budget_amount_local_micro')
resource_property(Campaign, 'duration_in_days', transform=TRANSFORM.INT)
resource_property(Campaign, 'end_time', transform=TRANSFORM.TIME)
resource_property(Campaign, 'entity_status')
resource_property(Campaign, 'frequency_cap', transform=TRANSFORM.INT)
resource_property(Campaign, 'funding_instrument_id')
resource_property(Campaign, 'name')
resource_property(Campaign, 'standard_delivery', transform=TRANSFORM.BOOL)
resource_property(Campaign, 'start_time', transform=TRANSFORM.TIME)
resource_property(Campaign, 'total_budget_amount_local_micro')
# sdk-only
resource_property(Campaign, 'to_delete', transform=TRANSFORM.BOOL)


class LineItem(Analytics, Resource, Persistence, Batch):

    PROPERTIES = {}

    BATCH_RESOURCE_COLLECTION = '/' + API_VERSION + '/batch/accounts/{account_id}/line_items'
    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/line_items'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/line_items/{id}'

    def targeting_criteria(self, id=None, **kwargs):
        """
        Returns a collection of targeting criteria available to the
        current line item.
        """
        self._validate_loaded()
        if id is None:
            return TargetingCriteria.all(self.account, line_item_ids=[self.id], **kwargs)
        else:
            return TargetingCriteria.load(self.account, id, **kwargs)

    def save(self):
        # automatically_select_bid and bid_type are exclusive parameters
        if self.automatically_select_bid and self.bid_type:
            if self.bid_type == 'AUTO':
                self.bid_type = None
                self.automatically_select_bid = True
            else:
                self.automatically_select_bid = None
        super(LineItem, self).save()


# line item properties
# read-only
resource_property(LineItem, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(LineItem, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(LineItem, 'id', readonly=True)
resource_property(LineItem, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
# writable
resource_property(LineItem, 'advertiser_domain')
resource_property(LineItem, 'advertiser_user_id')
resource_property(LineItem, 'automatically_select_bid', transform=TRANSFORM.BOOL)
resource_property(LineItem, 'bid_amount_local_micro')
resource_property(LineItem, 'bid_type')
resource_property(LineItem, 'bid_unit')
resource_property(LineItem, 'campaign_id')
resource_property(LineItem, 'categories', transform=TRANSFORM.LIST)
resource_property(LineItem, 'charge_by')
resource_property(LineItem, 'end_time', transform=TRANSFORM.TIME)
resource_property(LineItem, 'entity_status')
resource_property(LineItem, 'include_sentiment')
resource_property(LineItem, 'audience_expansion')
resource_property(LineItem, 'name')
resource_property(LineItem, 'objective')
resource_property(LineItem, 'optimization')
resource_property(LineItem, 'placements', transform=TRANSFORM.LIST)
resource_property(LineItem, 'primary_web_event_tag')
resource_property(LineItem, 'product_type')
resource_property(LineItem, 'start_time', transform=TRANSFORM.TIME)
resource_property(LineItem, 'total_budget_amount_local_micro')
resource_property(LineItem, 'tracking_tags')
# sdk-only
resource_property(LineItem, 'to_delete', transform=TRANSFORM.BOOL)


class LineItemApps(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/line_item_apps'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/line_item_apps/{id}'


resource_property(LineItemApps, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(LineItemApps, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(LineItemApps, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(LineItemApps, 'id', readonly=True)
resource_property(LineItemApps, 'os_type', readonly=True)
resource_property(LineItemApps, 'app_store_identifier', readonly=True)
resource_property(LineItemApps, 'line_item_id', readonly=True)


class LineItemPlacements(Resource):

    PROPERTIES = {}
    RESOURCE_COLLECTION = '/' + API_VERSION + '/line_items/placements'


resource_property(LineItemPlacements, 'product_type', readonly=True)
resource_property(LineItemPlacements, 'placements', readonly=True)


class ScheduledPromotedTweet(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/' + API_VERSION + '/accounts/{account_id}/scheduled_promoted_tweets'
    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/scheduled_promoted_tweets/{id}'


# scheduled promoted tweets properties
# read-only
resource_property(ScheduledPromotedTweet, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(ScheduledPromotedTweet, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(ScheduledPromotedTweet, 'id', readonly=True)
resource_property(ScheduledPromotedTweet, 'tweet_id', readonly=True)
resource_property(ScheduledPromotedTweet, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
# writable
resource_property(ScheduledPromotedTweet, 'line_item_id')
resource_property(ScheduledPromotedTweet, 'scheduled_tweet_id')


class Tweet(object):

    TWEET_CREATE = '/' + API_VERSION + '/accounts/{account_id}/tweet'

    def __init__(self):
        raise NotImplementedError(
            'Error! {name} cannot be instantiated.'.format(name=self.__class__.__name__))

    @classmethod
    @FlattenParams
    def create(klass, account, **kwargs):
        """
        Creates a "Promoted-Only" Tweet using the specialized Ads API end point.
        """
        resource = klass.TWEET_CREATE.format(account_id=account.id)
        response = Request(account.client, 'post', resource, params=kwargs).perform()
        return response.body['data']


class UserSettings(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/user_settings/{id}'


# user settings properties
# writable
resource_property(UserSettings, 'notification_email')
resource_property(UserSettings, 'contact_phone')
resource_property(UserSettings, 'contact_phone_extension')
resource_property(UserSettings, 'subscribed_email_types')
resource_property(UserSettings, 'user_id')


class TaxSettings(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/tax_settings'

    @classmethod
    def load(self, account):
        """
        Returns an object instance for a given account.
        """
        resource = self.RESOURCE.format(account_id=account.id)
        response = Request(account.client, 'get', resource).perform()
        return self(account).from_response(response.body['data'])

    def save(self):
        """
        Update the current object instance.
        """
        resource = self.RESOURCE.format(account_id=self.account.id)
        response = Request(
            self.account.client, 'put',
            resource, params=self.to_params()).perform()
        return self.from_response(response.body['data'])


# tax settings properties
# writable
resource_property(TaxSettings, 'address_city')
resource_property(TaxSettings, 'address_country')
resource_property(TaxSettings, 'address_email')
resource_property(TaxSettings, 'address_first_name')
resource_property(TaxSettings, 'address_last_name')
resource_property(TaxSettings, 'address_name')
resource_property(TaxSettings, 'address_postal_code')
resource_property(TaxSettings, 'address_region')
resource_property(TaxSettings, 'address_street1')
resource_property(TaxSettings, 'address_street2')
resource_property(TaxSettings, 'bill_to')
resource_property(TaxSettings, 'business_relationship')
resource_property(TaxSettings, 'client_address_city')
resource_property(TaxSettings, 'client_address_country')
resource_property(TaxSettings, 'client_address_email')
resource_property(TaxSettings, 'client_address_first_name')
resource_property(TaxSettings, 'client_address_last_name')
resource_property(TaxSettings, 'client_address_name')
resource_property(TaxSettings, 'client_address_postal_code')
resource_property(TaxSettings, 'client_address_region')
resource_property(TaxSettings, 'client_address_street1')
resource_property(TaxSettings, 'client_address_street2')
resource_property(TaxSettings, 'invoice_jurisdiction')
resource_property(TaxSettings, 'tax_category')
resource_property(TaxSettings, 'tax_exemption_id')
resource_property(TaxSettings, 'tax_id')


class ContentCategories(Resource):

    PROPERTIES = {}
    RESOURCE_COLLECTION = '/' + API_VERSION + '/content_categories'


resource_property(ContentCategories, 'id', readonly=True)
resource_property(ContentCategories, 'name', readonly=True)
resource_property(ContentCategories, 'iab_categories', readonly=True)


class IabCategories(Resource):

    PROPERTIES = {}
    RESOURCE_COLLECTION = '/' + API_VERSION + '/iab_categories'


resource_property(IabCategories, 'id', readonly=True)
resource_property(IabCategories, 'name', readonly=True)
resource_property(IabCategories, 'parent_id', readonly=True)
