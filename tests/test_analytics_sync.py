import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.client import Client
from twitter_ads.campaign import Campaign
from twitter_ads.enum import METRIC_GROUP, GRANULARITY
from twitter_ads import API_VERSION


@responses.activate
def test_analytics_sync_stats():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/stats/accounts/2iqph'),
                  body=with_fixture('analytics_sync_stats'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    ids = ['aaaa', 'bbbb']
    metric_groups = [METRIC_GROUP.ENGAGEMENT]
    stats = Campaign.all_stats(
        account,
        ids,
        metric_groups,
        granularity=GRANULARITY.TOTAL
    )

    assert len(responses.calls) == 2
    assert 'granularity=TOTAL' in responses.calls[1].request.url
    assert stats is not None
    assert isinstance(stats, list)
    assert len(stats) == 2
    assert stats[0]['id'] == 'aaaa'
