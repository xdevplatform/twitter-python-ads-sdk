# Copyright (C) 2015 Twitter, Inc.

"""Container for all plugable resource object logic used by the Ads API SDK."""

import dateutil.parser
import json

from datetime import datetime
from twitter_ads.utils import format_time
from twitter_ads.enum import ENTITY, TRANSFORM
from twitter_ads.http import Request
from twitter_ads.cursor import Cursor
from twitter_ads.utils import extract_response_headers, FlattenParams


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

    def from_response(self, response, headers=None):
        """
        Populates a given objects attributes from a parsed JSON API response.
        This helper handles all necessary type coercions as it assigns
        attribute values.
        """
        if headers is not None:
            limits = extract_response_headers(headers)
            for k in limits:
                setattr(self, k, limits[k])

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
                if not value:
                    continue
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

    @classmethod
    @FlattenParams
    def create(self, account, **kwargs):
        """
        Create a new item.
        """
        resource = self.RESOURCE_COLLECTION.format(account_id=account.id)
        response = Request(account.client, 'post', resource, params=kwargs).perform()
        return self(account).from_response(response.body['data'])

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
