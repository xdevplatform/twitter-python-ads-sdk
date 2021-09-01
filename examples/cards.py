from twitter_ads.client import Client
from twitter_ads.creative import Card
from twitter_ads.campaign import Tweet
from twitter_ads.restapi import UserIdLookup


CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# create the card
name = 'video website card'
components = [{"type":"MEDIA","media_key":"13_1191948012077092867"},{"type":"DETAILS","title":"Twitter","destination":{"type":"WEBSITE", "url":"http://twitter.com/"}}]
video_website_card = Card.create(account, name=name, components=components)

# get user_id for as_user_id parameter
user_id = UserIdLookup.load(account, screen_name='your_twitter_handle_name').id

# create a tweet using this new card
Tweet.create(account, text='Created from the SDK', as_user_id=user_id, card_uri=video_website_card.card_uri)
# https://twitter.com/apimctestface/status/1372283476615958529
