import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.client import Client
from twitter_ads.targeting import AudienceEstimate
from twitter_ads import API_VERSION


@responses.activate
def test_audience_summary():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.POST,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/audience_estimate'),
                  body=with_fixture('audience_estimate'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    params = {
        "targeting_criteria": [
          {
            "targeting_type":"LOCATION",
            "targeting_value":"96683cc9126741d1"
          },
          {
            "targeting_type":"BROAD_KEYWORD",
            "targeting_value":"cats"
          },
          {
            "targeting_type":"SIMILAR_TO_FOLLOWERS_OF_USER",
            "targeting_value": "14230524"
          },
          {
            "targeting_type":"SIMILAR_TO_FOLLOWERS_OF_USER",
            "targeting_value": "90420314"
          }
        ]
      }

    audience_summary = AudienceEstimate.load(
        account=account,
        params=params
    )

    print (audience_summary)
    assert audience_summary is not None
    assert audience_summary.audience_size is not None
    assert audience_summary.audience_size['min'] == 41133600
    assert audience_summary.audience_size['max'] == 50274400
