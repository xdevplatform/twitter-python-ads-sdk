from twitter_ads.client import Client
from twitter_ads.campaign import Tweet
from twitter_ads.creative import WebsiteCard

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
Tweet.preview(status='Hello @AdsAPI!')
Tweet.preview(status='Hello @AdsAPI!', media_ids=[634458428836962305, 634458428836962306])

# preview a new tweet with an embedded card
website_card = WebsiteCard.load(account, 'xyz1')
Tweet.preview(status='Hello @AdsAPI!', card_id=website_card.id)

# create a new null-casted tweet
Tweet.create(account, status='Hello from Python @AdsAPI!')
Tweet.create(account, status='Hello @AdsAPI!', media_ids=[634458428836962305, 634458428836962306])

# create a new null-casted tweet with an embedded card
website_card = WebsiteCard.load(account, 'xyz2')
Tweet.create(account, status='Hello @AdsAPI! {link}'.format(link=website_card.preview_url))
