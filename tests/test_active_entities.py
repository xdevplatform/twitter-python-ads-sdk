import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from datetime import datetime, timedelta
from twitter_ads.account import Account
from twitter_ads.client import Client
from twitter_ads.campaign import Campaign
from twitter_ads import API_VERSION


@responses.activate
def test_active_entities():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/stats/accounts/2iqph/active_entities'),
                  body=with_fixture('active_entities'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    end_time = datetime.utcnow().date()
    start_time = end_time - timedelta(days=1)

    active_entities = Campaign.active_entities(
        account,
        start_time,
        end_time,
        campaign_ids=['foo', 'bar']
    )

    assert len(responses.calls) == 2
    assert 'campaign_ids=foo%2Cbar' in responses.calls[1].request.url
    assert active_entities is not None
    assert isinstance(active_entities, list)
    assert len(active_entities) == 4
    assert active_entities[0]['entity_id'] == '2mvb28'
