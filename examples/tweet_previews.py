from twitter_ads.client import Client
from twitter_ads.creative import TweetPreview
from twitter_ads.enum import TWEET_TYPE

CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
ACCOUNT_ID = ''

# initialize the client
client = Client(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# fetch preview data
tweets = TweetPreview.load(
    account,
    tweet_ids=['1130942781109596160', '1101254234031370240'],
    tweet_type=TWEET_TYPE.PUBLISHED)

# iterate for each tweet
for k in tweets:
    print(k.tweet_id)
    print(k.preview)
