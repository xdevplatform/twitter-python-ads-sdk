# Copyright (C) 2015-2016 Twitter, Inc.

# note: the following is just a simple example. before making any stats calls, make
# sure to read our best practices for analytics which can be found here:
#
# https://dev.twitter.com/ads/analytics/best-practices
# https://dev.twitter.com/ads/analytics/metrics-and-segmentation
# https://dev.twitter.com/ads/analytics/metrics-derived

import sys
import time

from twitter_ads.client import Client
from twitter_ads.campaign import LineItem
from twitter_ads.enum import METRIC_GROUP
from twitter_ads.utils import split_list

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# grab the first 10 line items from Cursor
line_items = list(account.line_items(None))[:10]

# the list of metrics we want to fetch, for a full list of possible metrics
# see: https://dev.twitter.com/ads/analytics/metrics-and-segmentation
metric_groups = [METRIC_GROUP.BILLING]

# fetching stats on the instance
line_items[0].stats(metric_groups)

# fetching stats for multiple line items
ids = list(map(lambda x: x.id, line_items))
if not ids:
    print('Error: A minimum of 1 items must be provided for entity_ids')
    sys.exit()

sync_data = []
# Sync/Async endpoint can handle max 20 entity IDs per request
# so split the ids list into multiple requests
for chunk_ids in split_list(ids, 20):
    sync_data.append(LineItem.all_stats(account, chunk_ids, metric_groups))

print(sync_data)

# create async stats jobs and get job ids
queued_job_ids = []
for chunk_ids in split_list(ids, 20):
    queued_job_ids.append(LineItem.queue_async_stats_job(account, chunk_ids, metric_groups).id)

print(queued_job_ids)

# let the job complete
seconds = 30
time.sleep(seconds)

async_stats_job_results = LineItem.async_stats_job_result(account, job_ids=queued_job_ids)

async_data = []
for result in async_stats_job_results:
    async_data.append(LineItem.async_stats_job_data(account, url=result.url))

print(async_data)
