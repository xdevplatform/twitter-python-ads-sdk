from twitter_ads.client import Client
from twitter_ads.campaign import Campaign

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(id=ACCOUNT_ID)

# load and update a specific campaign
campaign = account.campaigns().next()
campaign.name = 'updated campaign name'
campaign.paused = True
campaign.save()

# iterate through campaigns
for campaign in account.campaigns():
    print(campaign.id)
