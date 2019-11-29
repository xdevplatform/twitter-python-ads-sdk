import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.creative import Tweets
from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads.enum import TWEET_TYPE
from twitter_ads import API_VERSION


@responses.activate
def test_tweets_get_all():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/tweets'),
                  body=with_fixture('tweets_get'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    tweets = Tweets.all(
        account,
        tweet_ids=['1166476031668015104'],
        tweet_type=TWEET_TYPE.PUBLISHED,
        trim_user=True
    )

    assert tweets is not None
    assert isinstance(tweets, Cursor)
    assert tweets.count == 1
    assert tweets.first['tweet_id'] == '1166476031668015104'
