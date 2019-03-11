# Copyright (C) 2015 Twitter, Inc.

"""Container for all plugable resource object logic used by the Ads API SDK."""

import dateutil.parser
from datetime import datetime, timedelta
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
import json

from twitter_ads.utils import format_time, to_time, validate_whole_hours
from twitter_ads.enum import ENTITY, GRANULARITY, PLACEMENT, TRANSFORM
from twitter_ads.http import Request
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION


def resource_property(klass, name, **kwargs):
    """Builds a resource object property."""
    klass.PROPERTIES[name] = kwargs

    def getter(self):
        return getattr(self, '_%s' % name, kwargs.get('default', None))

    if kwargs.get('readonly', False):
        setattr(klass, name, property(getter))
    else:
        def setter(self, value):
            setattr(self, '_%s' % name, value)
        setattr(klass, name, property(getter, setter))


class Resource(object):
    """Base class for all API resource objects."""

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account

    def from_response(self, response):
        """
        Populates a given objects attributes from a parsed JSON API response.
        This helper handles all necessary type coercions as it assigns
        attribute values.
        """
        for name in self.PROPERTIES:
            attr = '_{0}'.format(name)
            transform = self.PROPERTIES[name].get('transform', None)
            value = response.get(name, None)
            if transform and transform == TRANSFORM.TIME and value:
                setattr(self, attr, dateutil.parser.parse(value))
            if isinstance(value, int) and value == 0:
                continue  # skip attribute
            else:
                setattr(self, attr, value)

        return self

    def to_params(self):
        """
        Generates a Hash of property values for the current object. This helper
        handles all necessary type coercions as it generates its output.
        """
        params = {}
        for name in self.PROPERTIES:
            attr = '_{0}'.format(name)
            value = getattr(self, attr, None) or getattr(self, name, None)

            # skip attribute
            if value is None:
                continue

            if isinstance(value, datetime):
                params[name] = format_time(value)
            elif isinstance(value, list):
                params[name] = ','.join(map(str, value))
            elif isinstance(value, bool):
                params[name] = str(value).lower()
            else:
                params[name] = value

        return params

    @classmethod
    def all(klass, account, **kwargs):
        """Returns a Cursor instance for a given resource."""
        resource = klass.RESOURCE_COLLECTION.format(account_id=account.id)
        request = Request(account.client, 'get', resource, params=kwargs)
        return Cursor(klass, request, init_with=[account])

    @classmethod
    def load(klass, account, id, **kwargs):
        """Returns an object instance for a given resource."""
        resource = klass.RESOURCE.format(account_id=account.id, id=id)
        response = Request(account.client, 'get', resource, params=kwargs).perform()

        return klass(account).from_response(response.body['data'])

    def reload(self, **kwargs):
        """
        Reloads all attributes for the current object instance from the API.
        """
        if not self.id:
            return self

        resource = self.RESOURCE.format(account_id=self.account.id, id=self.id)
        response = Request(self.account.client, 'get', resource, params=kwargs).perform()

        return self.from_response(response.body['data'])

    def __repr__(self):
        return '<{name} resource at {mem} id={id}>'.format(
            name=self.__class__.__name__,
            mem=hex(id(self)),
            id=getattr(self, 'id', None)
        )

    def _validate_loaded(self):
        if not self.id:
            raise ValueError("""
            Error! {klass} object not yet initialized,
            call {klass}.load first.
            """).format(klass=self.__class__)

    def _load_resource(self, klass, id, **kwargs):
        self._validate_loaded()
        if id is None:
            return klass.all(self, **kwargs)
        else:
            return klass.load(self, id, **kwargs)


class Batch(object):

    _ENTITY_MAP = {
        'LineItem': ENTITY.LINE_ITEM,
        'Campaign': ENTITY.CAMPAIGN,
        'TargetingCriteria': ENTITY.TARGETING_CRITERION
    }

    @classmethod
    def batch_save(klass, account, objs):
        """
        Makes batch request(s) for a passed in list of objects
        """

        resource = klass.BATCH_RESOURCE_COLLECTION.format(account_id=account.id)

        json_body = []

        for obj in objs:
            entity_type = klass._ENTITY_MAP[klass.__name__].lower()
            obj_json = {'params': obj.to_params()}

            if obj.id is None:
                obj_json['operation_type'] = 'Create'
            elif obj.to_delete is True:
                obj_json['operation_type'] = 'Delete'
                obj_json['params'][entity_type + '_id'] = obj.id
            else:
                obj_json['operation_type'] = 'Update'
                obj_json['params'][entity_type + '_id'] = obj.id

            json_body.append(obj_json)

        resource = klass.BATCH_RESOURCE_COLLECTION.format(account_id=account.id)
        response = Request(account.client,
                           'post', resource,
                           body=json.dumps(json_body),
                           headers={'Content-Type': 'application/json'}).perform()

        # persist each entity
        for obj, res_obj in zip(objs, response.body['data']):
            obj = obj.from_response(res_obj)


class Persistence(object):
    """
    Container for all persistence related logic used by API resource objects.
    """

    def save(self):
        """
        Saves or updates the current object instance depending on the
        presence of `object.id`.
        """
        if self.id:
            method = 'put'
            resource = self.RESOURCE.format(account_id=self.account.id, id=self.id)
        else:
            method = 'post'
            resource = self.RESOURCE_COLLECTION.format(account_id=self.account.id)

        response = Request(
            self.account.client, method,
            resource, params=self.to_params()).perform()

        return self.from_response(response.body['data'])

    def delete(self):
        """
        Deletes the current object instance depending on the
        presence of `object.id`.
        """
        resource = self.RESOURCE.format(account_id=self.account.id, id=self.id)
        response = Request(self.account.client, 'delete', resource).perform()
        self.from_response(response.body['data'])


class Analytics(object):
    """
    Container for all analytics related logic used by API resource objects.
    """
    ANALYTICS_MAP = {
        'Campaign': ENTITY.CAMPAIGN,
        'FundingInstrument': ENTITY.FUNDING_INSTRUMENT,
        'LineItem': ENTITY.LINE_ITEM,
        'MediaCreative': ENTITY.MEDIA_CREATIVE,
        'OrganicTweet': ENTITY.ORGANIC_TWEET,
        'PromotedTweet': ENTITY.PROMOTED_TWEET
    }

    RESOURCE_SYNC = '/' + API_VERSION + '/stats/accounts/{account_id}'
    RESOURCE_ASYNC = '/' + API_VERSION + '/stats/jobs/accounts/{account_id}'
    RESOURCE_ACTIVE_ENTITIES = '/' + API_VERSION + '/stats/accounts/{account_id}/active_entities'

    def stats(self, metrics, **kwargs):  # noqa
        """
        Pulls a list of metrics for the current object instance.
        """
        return self.__class__.all_stats(self.account, [self.id], metrics, **kwargs)

    @classmethod
    def _standard_params(klass, ids, metric_groups, **kwargs):
        """
        Sets the standard params for a stats request
        """
        end_time = kwargs.get('end_time', datetime.utcnow())
        start_time = kwargs.get('start_time', end_time - timedelta(seconds=604800))
        granularity = kwargs.get('granularity', GRANULARITY.HOUR)
        placement = kwargs.get('placement', PLACEMENT.ALL_ON_TWITTER)

        params = {
            'metric_groups': ','.join(metric_groups),
            'start_time': to_time(start_time, granularity),
            'end_time': to_time(end_time, granularity),
            'granularity': granularity.upper(),
            'entity': klass.ANALYTICS_MAP[klass.__name__],
            'placement': placement
        }

        params['entity_ids'] = ','.join(ids)

        return params

    @classmethod
    def all_stats(klass, account, ids, metric_groups, **kwargs):
        """
        Pulls a list of metrics for a specified set of object IDs.
        """
        params = klass._standard_params(ids, metric_groups, **kwargs)

        resource = klass.RESOURCE_SYNC.format(account_id=account.id)
        response = Request(account.client, 'get', resource, params=params).perform()
        return response.body['data']

    @classmethod
    def queue_async_stats_job(klass, account, ids, metric_groups, **kwargs):
        """
        Queues a list of metrics for a specified set of object IDs asynchronously
        """
        params = klass._standard_params(ids, metric_groups, **kwargs)

        params['platform'] = kwargs.get('platform', None)
        params['country'] = kwargs.get('country', None)
        params['segmentation_type'] = kwargs.get('segmentation_type', None)

        resource = klass.RESOURCE_ASYNC.format(account_id=account.id)
        response = Request(account.client, 'post', resource, params=params).perform()
        return response.body['data']

    @classmethod
    def async_stats_job_result(klass, account, job_id, **kwargs):
        """
        Returns the results of the specified async job IDs
        """
        params = {
            'job_ids': job_id
        }

        resource = klass.RESOURCE_ASYNC.format(account_id=account.id)
        response = Request(account.client, 'get', resource, params=params).perform()

        return response.body['data'][0]

    @classmethod
    def async_stats_job_data(klass, account, url, **kwargs):
        """
        Returns the results of the specified async job IDs
        """
        resource = urlparse(url)
        domain = '{0}://{1}'.format(resource.scheme, resource.netloc)

        response = Request(account.client, 'get', resource.path, domain=domain,
                           raw_body=True, stream=True).perform()

        return response.body

    @classmethod
    def active_entities(klass, account, start_time, end_time, **kwargs):
        entity_type = klass.__name__
        if entity_type == 'OrganicTweet':
            raise ValueError("'OrganicTweet' not support with 'active_entities'")

        # The start and end times must be expressed in whole hours
        validate_whole_hours(start_time)
        validate_whole_hours(end_time)

        params = {
            'entity': klass.ANALYTICS_MAP[entity_type],
            'start_time': to_time(start_time, None),
            'end_time': to_time(end_time, None)
        }

        resource = klass.RESOURCE_ACTIVE_ENTITIES.format(account_id=account.id)
        response = Request(account.client, 'get', resource, params=params).perform()
        return response.body['data']
