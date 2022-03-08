# Copyright (C) 2015 Twitter, Inc.

from twitter_ads.client import Client
from twitter_ads.campaign import Tweet
from twitter_ads.creative import PromotedTweet, WebsiteCard
from twitter_ads.restapi import UserIdLookup

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'user access token'
ACCESS_TOKEN_SECRET = 'user access token secret'
ACCOUNT_ID = 'ads account id'

# initialize the twitter ads api client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load up the account instance, campaign and line item
account = client.accounts(ACCOUNT_ID)

# get user_id for as_user_id parameter
user_id = UserIdLookup.load(account, screen_name='your_twitter_handle_name').id

campaign = account.campaigns().next()
line_item = account.line_items(None, campaign_ids=campaign.id).next()

# create request for a simple nullcasted tweet
tweet1 = Tweet.create(account, text='There can be only one...', as_user_id=user_id)

# create request for a nullcasted tweet with a website card
website_card = WebsiteCard.all(account).next()
tweet2 = Tweet.create(
    account,
    text='Fine. There can be two.',
    as_user_id=user_id,
    card_uri=website_card.card_uri)

# promote the tweet using our line item
tweet_ids = [tweet1['id'], tweet2['id']]

response = PromotedTweet.attach(
    account,
    line_item_id=line_item.id,
    tweet_ids=tweet_ids
)

for i in response:
    print(i.id)
    print(i.tweet_id)
