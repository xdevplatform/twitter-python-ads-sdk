# Copyright (C) 2015 Twitter, Inc.

"""Container for all targeting related logic used by the Ads API SDK."""

from twitter_ads.http import Request
from twitter_ads import API_VERSION


class AudienceSummary(Resource, Persistence):
	PROPERTIES = {}

	RESOURCE = '/' + API_VERSION + '/accounts/{account_id}/audience_summary'

	def load(self, params):
		resource = self.RESOURCE.format(account_id=account.id)
		headers = {'Content-Type': 'application/json'}
        response = Request(self.account.client,
                           'post',
                           resource,
                           headers=headers,
                           body=json.dumps(params)).perform()
        return self.from_response(response.body['data'])