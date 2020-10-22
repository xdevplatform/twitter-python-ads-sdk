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

    assert isinstance(targeted_audiences, Cursor)
    assert isinstance(targeted_audiences.first.line_items, list)
    assert targeted_audiences.first.campaign_id  == '59hod'
    assert targeted_audiences.first.line_items[0]['id'] == '5gzog'
    assert targeted_audiences.first.line_items[0]['name'] == 'test-line-item'
    assert targeted_audiences.first.line_items[0]['servable'] == True
    assert len(responses.calls) == 3