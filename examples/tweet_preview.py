from twitter_ads.client import Client
from twitter_ads.campaign import Tweet
from twitter_ads.creative import WebsiteCard

"""
"Tweet.preview()" will no longer be available on August 20, 2019.
 https://twittercommunity.com/t/announcement-new-and-improved-tweet-previews/126064

Please use "TweetPreview.load()" instead. See examples/tweet_previews.py for reference.
"""


CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(
    CONSUMER_KEY,
    CONSUMER_SECRET,
    ACCESS_TOKEN,
    ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# preview an existing tweet
Tweet.preview(account, id=661845592138776576)

# preview a new tweet
Tweet.preview(account, text='Hello @AdsAPI!')
Tweet.preview(account, text='Hello @AdsAPI!', media_ids=[634458428836962305, 634458428836962306])

# preview a new tweet with an embedded card
website_card = WebsiteCard.all(account).next()
Tweet.preview(account, text='Hello @AdsAPI!', card_id=website_card.id)

# create a new null-casted tweet
Tweet.create(account, text='Hello from Python @AdsAPI!')
Tweet.create(account, text='Hello @AdsAPI!', media_ids=[634458428836962305, 634458428836962306])

# create a new null-casted tweet with an embedded card
website_card = WebsiteCard.all(account).next()
Tweet.create(account, text='Hello @AdsAPI! {link}'.format(link=website_card.preview_url))
