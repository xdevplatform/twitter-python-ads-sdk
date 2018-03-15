from twitter_ads.campaign import Tweet
from twitter_ads.client import Client
from twitter_ads.creative import MediaLibrary, PollCard
from twitter_ads.enum import MEDIA_TYPE


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
ACCOUNT_ID = ''

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# most recent Media Library video
ml = MediaLibrary(account).all(account, media_type=MEDIA_TYPE.VIDEO)
media_key = ml.first.media_key

# create Poll Card with video
pc = PollCard(account)
pc.duration_in_minutes = 10080 # one week
pc.first_choice = 'Northern'
pc.second_choice = 'Southern'
pc.name = ml.first.name + ' poll card from SDK'
pc.media_key = media_key
pc.save()

# create Tweet
Tweet.create(account, text='Which hemisphere do you prefer?', card_uri=pc.card_uri)
# https://twitter.com/apimctestface/status/973002610033610753
