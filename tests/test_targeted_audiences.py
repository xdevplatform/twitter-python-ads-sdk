import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.client import Client
from twitter_ads.audience import TailoredAudience
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION


@responses.activate
def test_targeted_audiences():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'))

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/tailored_audiences/2906h'),
                  body=with_fixture('tailored_audiences_load'))

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/tailored_audiences/abc2/targeted?with_active=True'),
                  body=with_fixture('targeted_audiences'))

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    audience = TailoredAudience.load(account, '2906h')
    targeted_audiences = audience.targeted(
        with_active=True
    )

    for campaign in targeted_audiences:
        assert campaign.campaign_id == '59hod'
        assert isinstance(campaign.line_items, Cursor)
    
    # assert len(responses.calls) == 2
    # assert 'campaign_ids=foo%2Cbar' in responses.calls[1].request.url
    # assert active_entities is not None
    # assert isinstance(active_entities, list)
    # assert len(active_entities) == 4
    # assert active_entities[0]['entity_id'] == '2mvb28'
