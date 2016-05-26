# Copyright (C) 2015-2016 Twitter, Inc.

# note: the following is just a simple example. before making any stats calls, make
# sure to read our best practices for analytics which can be found here:
#
# https://dev.twitter.com/ads/analytics/best-practices
# https://dev.twitter.com/ads/analytics/metrics-and-segmentation
# https://dev.twitter.com/ads/analytics/metrics-derived

import time

from twitter_ads.client import Client
from twitter_ads.campaign import LineItem
from twitter_ads.enum import METRIC_GROUP

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
metric_groups = [METRIC_GROUP.BILLING]

# fetching stats on the instance
line_items[0].stats(metric_groups)

# fetching stats for multiple line items
ids = map(lambda x: x.id, line_items)
LineItem.all_stats(account, ids, metric_groups)

# fetching async stats on the instance
queued_job = LineItem.queue_async_stats_job(account, ids, metric_groups)

# get the job_id:
job_id = queued_job['id']

# let the job complete
seconds = 15
time.sleep(seconds)

async_stats_job_result = LineItem.async_stats_job_result(account, job_id)

async_data = LineItem.async_stats_job_data(account, async_stats_job_result['url'])
