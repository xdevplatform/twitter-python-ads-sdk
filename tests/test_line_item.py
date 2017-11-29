import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.campaign import LineItem
from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION


@responses.activate
def test_line_items_all():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/line_items'),
                  body=with_fixture('line_items_all'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    cursor = account.line_items()
    assert cursor is not None
    assert isinstance(cursor, Cursor)
    assert cursor.count == 10

    lineitem = cursor.next()
    assert lineitem.id == 'bw2'
    assert lineitem.entity_status == 'ACTIVE'


@responses.activate
def test_line_item_load():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/line_items/bw2'),
                  body=with_fixture('line_items_load'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    line_item = LineItem.load(account, 'bw2')
    assert line_item.id == 'bw2'
    assert line_item.entity_status == 'ACTIVE'
