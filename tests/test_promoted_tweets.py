import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.client import Client
from twitter_ads.creative import PromotedTweet
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION


@responses.activate
def test_promoted_tweets_all():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/promoted_tweets'),
                  body=with_fixture('promoted_tweets_all'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    cursor = PromotedTweet.all(account)
    assert cursor is not None
    assert isinstance(cursor, Cursor)
    assert cursor.count == 20

    promoted_tweet = cursor.next()
    assert promoted_tweet.id == '6thl4'
    assert promoted_tweet.entity_status == 'ACTIVE'


@responses.activate
def test_promoted_tweets_load():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/promoted_tweets/6thl4'),
                  body=with_fixture('promoted_tweets_load'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    promoted_tweet = PromotedTweet.load(account, '6thl4')
    assert promoted_tweet.id == '6thl4'
    assert promoted_tweet.entity_status == 'ACTIVE'
