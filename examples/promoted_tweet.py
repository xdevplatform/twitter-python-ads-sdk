# Copyright (C) 2015 Twitter, Inc.

from twitter_ads.client import Client
from twitter_ads.campaign import Tweet
from twitter_ads.creative import PromotedTweet, WebsiteCard

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'user access token'
ACCESS_TOKEN_SECRET = 'user access token secret'
ADS_ACCOUNT = 'ads account id'

# initialize the twitter ads api client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load up the account instance, campaign and line item
account = client.accounts(ADS_ACCOUNT)
campaign = account.campaigns().next()
line_item = account.line_items(None, campaign_ids=campaign.id).next()

# create request for a simple nullcasted tweet
tweet1 = Tweet.create(account, text='There can be only one...')

# promote the tweet using our line item
promoted_tweet = PromotedTweet(account)
promoted_tweet.line_item_id = line_item.id
promoted_tweet.tweet_id = tweet1['id']
promoted_tweet.save()

# create request for a nullcasted tweet with a website card
website_card = WebsiteCard.all(account).next()
text = "Fine. There can be two. {card_url}".format(card_url=website_card.preview_url)
tweet2 = Tweet.create(account, text)

# promote the tweet using our line item
promoted_tweet = PromotedTweet(account)
promoted_tweet.line_item_id = line_item.id
promoted_tweet.tweet_id = tweet2['id']
promoted_tweet.save()
