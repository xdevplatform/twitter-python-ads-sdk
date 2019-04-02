# Copyright (C) 2015 Twitter, Inc.

from twitter_ads import API_VERSION
from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads.http import Request
from twitter_ads.error import Error

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'user access token'
ACCESS_TOKEN_SECRET = 'user access token secret'
ADS_ACCOUNT = 'ads account id'

# initialize the twitter ads api client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load up the account instance
account = client.accounts(ADS_ACCOUNT)

# using the Request object you can manually request any
# twitter ads api resource that you want.

resource = '/' + API_VERSION + '/accounts/{account_id}/features'.format(account_id=account.id)
params = {'feature_keys': 'AGE_TARGETING,CPI_CHARGING'}

# try, build and execute the request with error handling
try:
    response = Request(client, 'get', resource, params=params).perform()
    print(response.body['data'][0])
except Error as e:
    # see twitter_ads.error for more details
    print e.details
    raise

# you can also manually construct requests to be
# used in Cursor objects.

resource = '/' + API_VERSION + '/targeting_criteria/locations'
params = {'location_type': 'CITIES', 'q': 'port'}
request = Request(client, 'get', resource, params=params)
cursor = Cursor(None, request)

# execute requests and iterate cursor until exhausted
for obj in cursor:
    print(obj['name'])
