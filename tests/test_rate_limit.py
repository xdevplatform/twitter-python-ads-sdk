import responses
import unittest
import time

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.campaign import Campaign
from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads.http import Request
from twitter_ads.resource import Resource
from twitter_ads import API_VERSION
from twitter_ads.error import RateLimit


@responses.activate
def test_rate_limit_handle_with_retry_success_1(monkeypatch):
    # scenario:
    #  - 500 (retry) -> 429 (handle rate limit) -> 200 (end)
    monkeypatch.setattr(time, 'sleep', lambda s: None)

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=500,
                  body=with_fixture('campaigns_all'),
                  content_type='application/json',
                  headers={
                      'x-account-rate-limit-limit': '10000',
                      'x-account-rate-limit-remaining': '0',
                      'x-account-rate-limit-reset': '1546300800'
                  })

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=429,
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
            'handle_rate_limit': True,
            'retry_max': 1,
            'retry_delay': 3000,
            'retry_on_status': [500]
        }
    )

    account = Account.load(client, '2iqph')

    cursor = Campaign.all(account)
    assert len(responses.calls) == 4
    assert cursor is not None
    assert isinstance(cursor, Cursor)
    assert cursor.account_rate_limit_limit == '10000'
    assert cursor.account_rate_limit_remaining == '9999'
    assert cursor.account_rate_limit_reset == '1546300800'


@responses.activate
def test_rate_limit_handle_with_retry_success_2(monkeypatch):
    # scenario:
    #  - 429 (handle rate limit) -> 500 (retry) -> 200 (end)
    monkeypatch.setattr(time, 'sleep', lambda s: None)

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=429,
                  body=with_fixture('campaigns_all'),
                  content_type='application/json',
                  headers={
                      'x-account-rate-limit-limit': '10000',
                      'x-account-rate-limit-remaining': '0',
                      'x-account-rate-limit-reset': '1546300800'
                  })

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=500,
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
            'handle_rate_limit': True,
            'retry_max': 1,
            'retry_delay': 3000,
            'retry_on_status': [500]
        }
    )

    account = Account.load(client, '2iqph')

    cursor = Campaign.all(account)
    assert len(responses.calls) == 4
    assert cursor is not None
    assert isinstance(cursor, Cursor)
    assert cursor.account_rate_limit_limit == '10000'
    assert cursor.account_rate_limit_remaining == '9999'
    assert cursor.account_rate_limit_reset == '1546300800'


@responses.activate
def test_rate_limit_handle_success(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda s: None)

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=429,
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
            'handle_rate_limit': True
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
def test_rate_limit_handle_error(monkeypatch):
    monkeypatch.setattr(time, 'sleep', lambda s: None)

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=429,
                  body=with_fixture('campaigns_all'),
                  content_type='application/json',
                  headers={
                      'x-account-rate-limit-limit': '10000',
                      'x-account-rate-limit-remaining': '0',
                      'x-account-rate-limit-reset': str(int(time.time()) + 5)
                  })

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                  status=429,
                  body=with_fixture('campaigns_all'),
                  content_type='application/json',
                  headers={
                      'x-account-rate-limit-limit': '10000',
                      'x-account-rate-limit-remaining': '0',
                      'x-account-rate-limit-reset': '1546300800'
                  })

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40),
        options={
            'handle_rate_limit': True
        }
    )

    account = Account.load(client, '2iqph')

    try:
        cursor = Campaign.all(account)
    except Exception as e:
        error = e
        print(error)
    assert len(responses.calls) == 3
    assert isinstance(error, RateLimit)
    assert error.reset_at == '1546300800'


@responses.activate
def test_rate_limit_cursor_class_access():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
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
        characters(40)
    )

    account = Account.load(client, '2iqph')

    cursor = Campaign.all(account)
    assert cursor is not None
    assert isinstance(cursor, Cursor)
    assert cursor.account_rate_limit_limit == '10000'
    assert cursor.account_rate_limit_remaining == '9999'
    assert cursor.account_rate_limit_reset == '1546300800'


@responses.activate
def test_rate_limit_resource_class_access():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns/2wap7'),
                  body=with_fixture('campaigns_load'),
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
        characters(40)
    )

    account = Account.load(client, '2iqph')
    campaign = Campaign.load(account, '2wap7')

    resource = '/' + API_VERSION + '/accounts/2iqph/campaigns/2wap7'
    params = {}

    response = Request(client, 'get', resource, params=params).perform()
    # from_response() is a staticmethod, so passing campaign instance as dummy.
    # We can later change this test case to not call this manually
    # once we changed existing classes to pass the header argument.
    data = campaign.from_response(response.body['data'], response.headers)

    assert data is not None
    assert isinstance(data, Resource)
    assert data.id == '2wap7'
    assert data.entity_status == 'ACTIVE'
    assert data.account_rate_limit_limit == '10000'
    assert data.account_rate_limit_remaining == '9999'
    assert data.account_rate_limit_reset == '1546300800'
