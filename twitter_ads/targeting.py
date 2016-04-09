# Copyright (C) 2015 Twitter, Inc.

"""Container for all targeting related logic used by the Ads API SDK."""

from twitter_ads.http import Request


class ReachEstimate(object):

    RESOURCE = '/1/accounts/{account_id}/reach_estimate'

    @classmethod
    def fetch(klass, account, product_type, objective, user_id, **kwargs):
        params = {'product_type': product_type, 'objective': objective, 'user_id': user_id}
        params.update(kwargs)

        resource = klass.RESOURCE.format(account_id=account.id)
        response = Request(account.client, 'get', resource, params=params).perform()

        return response.body['data']
