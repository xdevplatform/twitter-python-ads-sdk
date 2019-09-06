import responses
import unittest
import time

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.campaign import Campaign
from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION
from twitter_ads.error import NotFound


@responses.activate
def test_retry_count_success(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda s: None)

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=404,
                  body=with_fixture('campaigns_all'),
                  content_type='application/json',
                  headers={
                      'x-account-rate-limit-limit': '10000',
                      'x-account-rate-limit-remaining': '0',
                      'x-account-rate-limit-reset': str(int(time.time()) + 5)
                  })

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=200,
                  body=with_fixture('campaigns_all'),
                  content_type='application/json',
                  headers={
                      'x-account-rate-limit-limit': '10000',
                      'x-account-rate-limit-remaining': '9999',
                      'x-account-rate-limit-reset': '1546300800'
                  })

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40),
        options={
            'retry_max': 1,
            'retry_delay': 3000,
            'retry_on_status': [404, 500, 503]
        }
    )

    account = Account.load(client, '2iqph')

    cursor = Campaign.all(account)
    assert len(responses.calls) == 3
    assert cursor is not None
    assert isinstance(cursor, Cursor)
    assert cursor.account_rate_limit_limit == '10000'
    assert cursor.account_rate_limit_remaining == '9999'
    assert cursor.account_rate_limit_reset == '1546300800'


@responses.activate
def test_retry_count_error(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda s: None)

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=404,
                  body=with_fixture('campaigns_all'),
                  content_type='application/json',
                  headers={
                      'x-account-rate-limit-limit': '10000',
                      'x-account-rate-limit-remaining': '0',
                      'x-account-rate-limit-reset': str(int(time.time()) + 5)
                  })

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=404,
                  body=with_fixture('campaigns_all'),
                  content_type='application/json',
                  headers={
                      'x-account-rate-limit-limit': '10000',
                      'x-account-rate-limit-remaining': '9999',
                      'x-account-rate-limit-reset': '1546300800'
                  })

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40),
        options={
            'retry_max': 1,
            'retry_delay': 3000,
            'retry_on_status': [404, 500, 503]
        }
    )

    account = Account.load(client, '2iqph')

    try:
        cursor = Campaign.all(account)
    except Exception as e:
        error = e
        print(error)
    assert len(responses.calls) == 3
    assert isinstance(error, NotFound)
