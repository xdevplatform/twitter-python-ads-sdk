# Copyright (C) 2015 Twitter, Inc.

"""Container for all campaign management logic used by the Ads API SDK."""

from twitter_ads.resource import resource, Resource, Persistence, Analytics
from twitter_ads.http import Request
from twitter_ads.cursor import Cursor


@resource
class TargetingCriteria(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'name': {'readonly': True},
        'localized_name': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        'deleted': {'readonly': True},
        # writable
        'line_item_id': {},
        'targeting_type': {},
        'targeting_value': {},
        'tailored_audience_expansion': {},
        'tailored_audience_type': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/targeting_criteria'
    RESOURCE = '/0/accounts/{account_id}/targeting_criteria/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account

    @classmethod
    def all(klass, account, line_item_id, **kwargs):
        """Returns a Cursor instance for a given resource."""
        params = {'line_item_id': line_item_id}
        params.update(kwargs)

        resource = klass.RESOURCE_COLLECTION.format(account_id=account.id)
        request = Request(account.client(), 'get', resource, params=params)

        return Cursor(klass, request, init_with=[account])


@resource
class FundingInstrument(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'name': {'readonly': True},
        'cancelled': {'readonly': True},
        'credit_limit_local_micro': {'readonly': True},
        'currency': {'readonly': True},
        'description': {'readonly': True},
        'funded_amount_local_micro': {'readonly': True},
        'type': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        'deleted': {'readonly': True}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/funding_instruments'
    RESOURCE = '/0/accounts/{account_id}/funding_instruments/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class PromotableUser(Resource):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'promotable_user_type': {'readonly': True},
        'user_id': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        'deleted': {'readonly': True}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/promotable_users'
    RESOURCE = '/0/accounts/{account_id}/promotable_users/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class AppList(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'apps': {'readonly': True},
        'name': {'readonly': True}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/app_lists'
    RESOURCE = '/0/accounts/{account_id}/app_lists/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account

    def create(self, name, *ids):
        if isinstance(ids, list):
            ids = ','.join(map(str, ids))

        resource = self.RESOURCE_COLLECTION.format(account_id=self.account.id)
        params = self.to_params.update({
            'app_store_identifiers': ids, 'name': name})
        response = Request(
            self.account.client(), 'post', resource, params=params).perform()

        return self.from_response(response.body['data'])

    def apps(self):
        if self.id and not hasattr(self, '_apps'):
            self.reload()
        return self._apps


@resource
class Campaign(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'reasons_not_servable': {'readonly': True},
        'servable': {'readonly': True},
        'deleted': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        # writable
        'name': {},
        'funding_instrument_id': {},
        'end_time': {'transform': 'time'},
        'start_time': {'transform': 'time'},
        'paused': {},
        'currency': {},
        'standard_delivery': {},
        'daily_budget_amount_local_micro': {},
        'total_budget_amount_local_micro': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/campaigns'
    RESOURCE_STATS = '/0/stats/accounts/{account_id}/campaigns'
    RESOURCE = '/0/accounts/{account_id}/campaigns/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class LineItem(Resource, Persistence, Analytics):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        'deleted': {'readonly': True},
        # writable
        'name': {},
        'campaign_id': {},
        'advertiser_domain': {},
        'categories': {},
        'charge_by': {},
        'include_sentiment': {},
        'objective': {},
        'optimization': {},
        'paused': {},
        'primary_web_event_tag': {},
        'product_type': {},
        'placements': {},
        'bid_unit': {},
        'automatically_select_bid': {},
        'bid_amount_local_micro': {},
        'total_budget_amount_local_micro': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/line_items'
    RESOURCE_STATS = '/0/stats/accounts/{account_id}/line_items'
    RESOURCE = '/0/accounts/{account_id}/line_items/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account

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
