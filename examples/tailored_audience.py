from twitter_ads.client import Client
from twitter_ads.audience import TailoredAudience
from twitter_ads.enum import TA_LIST_TYPES, TA_OPERATIONS

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# create a new tailored audience
audience = TailoredAudience.create(account, '/path/to/file', 'my list', TA_LIST_TYPES.EMAIL)

# check the processing status
audience.status()

# update the tailored audience
audience.update('/path/to/file', TA_LIST_TYPES.TWITTER_ID, TA_OPERATIONS.REMOVE)
audience.update('/path/to/file', TA_LIST_TYPES.PHONE_NUMBER, TA_OPERATIONS.ADD)

# delete the tailored audience
audience.delete()

# add users to the account's global opt-out list
TailoredAudience.opt_out(account, '/path/to/file', TA_OPERATIONS.HANDLE)
