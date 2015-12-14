# Copyright (C) 2015 Twitter, Inc.

"""Container for all plugable resource object logic used by the Ads API SDK."""

import datetime
import dateutil.parser

from twitter_ads.utils import format_time, to_time
from twitter_ads.enum import TRANSFORM, GRANULARITY
from twitter_ads.http import Request
from twitter_ads.cursor import Cursor


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

    PROPERTIES = {}

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

            if isinstance(value, datetime.datetime):
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
        request = Request(account.client(), 'get', resource, params=kwargs)
        return Cursor(klass, request, init_with=[account])

    @classmethod
    def load(klass, account, id, **kwargs):
        """Returns an object instance for a given resource."""
        resource = klass.RESOURCE.format(account_id=account.id, id=id)
        response = Request(
            account.client(), 'get', resource, params=kwargs).perform()

        return klass(account).from_response(response.body['data'])

    def reload(self, **kwargs):
        """
        Reloads all attributes for the current object instance from the API.
        """
        if not self.id:
            return self

        resource = self.RESOURCE.format(
            account_id=self.account.id, id=self.id)
        response = Request(
            self.account.client(), 'get', resource, params=kwargs).perform()

        self.from_response(response.body['data'])

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
            resource = self.RESOURCE.format(
                account_id=self.account.id, id=self.id)
        else:
            method = 'post'
            resource = self.RESOURCE_COLLECTION.format(
                account_id=self.account.id)

        response = Request(
            self.account.client(), method,
            resource, params=self.to_params()).perform()

        self.from_response(response.body['data'])

    def delete(self):
        """
        Deletes the current object instance depending on the
        presence of `object.id`.
        """
        resource = self.RESOURCE.format(account_id=self.account.id, id=self.id)
        response = Request(self.account.client(), 'delete', resource).perform()
        self.from_response(response.body['data'])


class Analytics(object):
    """
    Container for all analytics related logic used by API resource objects.
    """

    ANALYTICS_MAP = {
        'LineItem': 'line_item_ids',
        'OrganicTweet': 'tweet_ids',
        'Tweet': 'tweet_ids',
        'PromotedTweet': 'promoted_tweet_ids'
    }

    def stats(self, metrics, **kwargs):  # noqa
        """
        Pulls a list of metrics for the current object instance.
        """
        return self.__class__.all_stats(self.account, [self.id], metrics, **kwargs)

    @classmethod
    def all_stats(klass, account, ids, metrics, **kwargs):
        """
        Pulls a list of metrics for a specified set of object IDs.
        """
        end_time = kwargs.get('end_time', datetime.datetime.utcnow())
        start_time = kwargs.get('start_time', end_time - datetime.timedelta(seconds=604800))
        granularity = kwargs.get('granularity', GRANULARITY.HOUR)
        segmentation_type = kwargs.get('segmentation_type', None)

        params = {
            'metrics': ','.join(metrics),
            'start_time': to_time(start_time, granularity),
            'end_time': to_time(end_time, granularity),
            'granularity': granularity.upper()
        }
        if segmentation_type is not None:
            params['segmentation_type'] = segmentation_type.upper()

        params[klass.ANALYTICS_MAP[klass.__name__]] = ','.join(ids)

        resource = klass.RESOURCE_STATS.format(account_id=account.id)
        response = Request(account.client(), 'get', resource, params=params).perform()
        return response.body['data']
