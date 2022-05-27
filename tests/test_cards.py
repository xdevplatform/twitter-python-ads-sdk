import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.campaign import Campaign
from twitter_ads.creative import Card
from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION


@responses.activate
def test_cards_all():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/cards'),
                  body=with_fixture('cards_all'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    cursor = Card.all(account)
    assert cursor is not None
    assert isinstance(cursor, Cursor)

    card = cursor.next()
    assert card.id == '1340029888649076737'
    assert card.card_type == 'VIDEO_WEBSITE'
    assert len(card.components) == 2


@responses.activate
def test_card_load():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/cards/1503831318555086849'),
                  body=with_fixture('cards_load'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    card = Card.load(account, '1503831318555086849')
    assert card.id == '1503831318555086849'
    assert card.card_type == 'VIDEO_WEBSITE'
    assert card.card_uri == 'card://1503831318555086849'
