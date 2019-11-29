import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.creative import TweetPreview
from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads.enum import TWEET_TYPE
from twitter_ads import API_VERSION


@responses.activate
def test_tweet_previews_load():
    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph'),
                  body=with_fixture('accounts_load'),
                  content_type='application/json')

    responses.add(responses.GET,
                  with_resource('/' + API_VERSION + '/accounts/2iqph/tweet_previews'),
                  body=with_fixture('tweet_previews'),
                  content_type='application/json')

    client = Client(
        characters(40),
        characters(40),
        characters(40),
        characters(40)
    )

    account = Account.load(client, '2iqph')

    tweets = TweetPreview.load(
        account,
        tweet_ids=['1130942781109596160', '1101254234031370240'],
        tweet_type=TWEET_TYPE.PUBLISHED)

    assert tweets is not None
    assert isinstance(tweets, Cursor)
    assert tweets.count == 2
    
    tweet = tweets.next()
    assert tweet.tweet_id == '1130942781109596160'
    assert '<iframe' in tweet.preview
