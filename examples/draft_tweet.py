from twitter_ads.client import Client
from twitter_ads.campaign import Tweet
from twitter_ads.creative import DraftTweet


CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'user access token'
ACCESS_TOKEN_SECRET = 'user access token secret'
ACCOUNT_ID = 'ads account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# fetch draft tweets from a given account
tweets = DraftTweet.all(account)
for tweet in tweets:
    print(tweet.id_str)
    print(tweet.text)

# create a new draft tweet
draft_tweet = DraftTweet(account)
draft_tweet.text = 'draft tweet - new'
draft_tweet = draft_tweet.save()
print(draft_tweet.id_str)
print(draft_tweet.text)

# fetch single draft tweet metadata
tweet_id = draft_tweet.id_str
draft_tweet = draft_tweet.load(account, tweet_id)
print(draft_tweet.id_str)
print(draft_tweet.text)

# update (PUT) metadata
draft_tweet.text = 'draft tweet - update'
draft_tweet = draft_tweet.save()
print(draft_tweet.id_str)
print(draft_tweet.text)

# preview draft tweet of current instance (send notification)
draft_tweet.preview()
# or, specify any draft_tweet_id
# draft_tweet.preview(draft_tweet_id='1142020720651673600')

# create a nullcasted tweet using draft tweet metadata
tweet = Tweet.create(account, text=draft_tweet.text)
print(tweet)

# delete draft tweet
# draft_tweet.delete()
