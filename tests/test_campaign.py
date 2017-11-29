import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.campaign import Campaign
from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION


@responses.activate
def test_campaigns_all():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  body=with_fixture('campaigns_all'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    cursor = account.campaigns()
    assert cursor is not None
    assert isinstance(cursor, Cursor)
    assert cursor.count == 10

    campaign = cursor.next()
    assert campaign.id == '2wap7'
    assert campaign.entity_status == 'ACTIVE'


@responses.activate
def test_campaign_load():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns/2wap7'),
                  body=with_fixture('campaigns_load'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    campaign = Campaign.load(account, '2wap7')
    assert campaign.id == '2wap7'
    assert campaign.entity_status == 'ACTIVE'
