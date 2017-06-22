import datetime

from twitter_ads.client import Client
from twitter_ads.audience import TailoredAudience
from twitter_ads.enum import TA_LIST_TYPES, TA_OPERATIONS

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the twitter ads api client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load up the account instance
account = client.accounts(ADS_ACCOUNT)


# set the current date/time
now = datetime.datetime.utcnow()
effective_at = now.strftime("%Y-%m-%dT%H:%M:%SZ")

# setting expiration to 100 years in the future
expires_at = (now + datetime.timedelta(days=365*100)).strftime("%Y-%m-%dT%H:%M:%SZ")



audience = TailoredAudience.ta_file_upload(account, '/path/to/file', "audiencetest", TA_LIST_TYPES.DEVICE_ID, expires_at, effective_at)

print audience