# Copyright (C) 2015 Twitter, Inc.

"""Container for all targeting related logic used by the Ads API SDK."""

from twitter_ads.http import Request
from twitter_ads.resource import resource_property, Resource, Persistence
from twitter_ads import API_VERSION
from twitter_ads.utils import FlattenParams
import json


class AudienceEstimate(Resource, Persistence):
    PROPERTIES = {}

    RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/audience_estimate'

    @classmethod
    @FlattenParams
    def load(klass, account, params):
        resource = klass.RESOURCE.format(account_id=account.id)
        headers = {'Content-Type': 'application/json'}
        response = Request(account.client,
                           'post',
                           resource,
                           headers=headers,
                           body=json.dumps(params)).perform()
        return klass(account).from_response(response.body['data'])


resource_property(AudienceEstimate, 'audience_size')
