from datetime import datetime, timedelta

from twitter_ads.client import Client
from twitter_ads.campaign import ScheduledPromotedTweet
from twitter_ads.creative import ScheduledTweet
from twitter_ads.restapi import UserIdLookup

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'user access token'
ACCESS_TOKEN_SECRET = 'user access token secret'
ACCOUNT_ID = 'ads account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# get user_id for as_user_id parameter
user_id = UserIdLookup.load(account, screen_name='your_twitter_handle_name').id

# create the Scheduled Tweet
scheduled_tweet = ScheduledTweet(account)
scheduled_tweet.text = 'Future'
scheduled_tweet.as_user_id = user_id
scheduled_tweet.scheduled_at = datetime.utcnow() + timedelta(days=2)
scheduled_tweet.save()

# associate with a line item
account.line_items().next().id
scheduled_promoted_tweet = ScheduledPromotedTweet(account)
scheduled_promoted_tweet.line_item_id = line_item_id
scheduled_promoted_tweet.scheduled_tweet_id = scheduled_tweet.id
scheduled_promoted_tweet.save()
