from datetime import datetime, timedelta

from twitter_ads.client import Client
from twitter_ads.creative import ScheduledTweet

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# create the Scheduled Tweet
scheduled_tweet = ScheduledTweet(account)
scheduled_tweet.text = 'Future'
scheduled_tweet.scheduled_at = datetime.utcnow() + timedelta(days=2)
scheduled_tweet.save()
