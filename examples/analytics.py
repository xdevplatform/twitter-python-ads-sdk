# Copyright (C) 2015 Twitter, Inc.

# note: the following is just a simple example. before making any stats calls, make
# sure to read our best practices for analytics which can be found here:
#
# https://dev.twitter.com/ads/analytics/best-practices
# https://dev.twitter.com/ads/analytics/metrics-and-segmentation
# https://dev.twitter.com/ads/analytics/metrics-derived

from twitter_ads.client import Client
from twitter_ads.campaign import LineItem

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# limit request count and grab the first 10 line items from Cursor
line_items = list(account.line_items(None, count=10))[:10]

# the list of metrics we want to fetch, for a full list of possible metrics
# see: https://dev.twitter.com/ads/analytics/metrics-and-segmentation
metrics = ['billed_engagements', 'billed_follows']

# fetching stats on the instance
line_items[0].stats(metrics)

# fetching stats for multiple line items
ids = map(lambda x: x.id, line_items)
LineItem.all_stats(account, ids, metrics)
