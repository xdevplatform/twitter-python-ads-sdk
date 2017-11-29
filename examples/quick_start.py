from datetime import datetime

from twitter_ads.client import Client
from twitter_ads.campaign import Campaign, LineItem, TargetingCriteria
from twitter_ads.enum import ENTITY_STATUS, OBJECTIVE, PLACEMENT, PRODUCT

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# create your campaign
campaign = Campaign(account)
campaign.funding_instrument_id = account.funding_instruments().next().id
campaign.daily_budget_amount_local_micro = 1000000
campaign.name = 'my first campaign'
campaign.entity_status = ENTITY_STATUS.PAUSED
campaign.start_time = datetime.utcnow()
campaign.save()

# create a line item for the campaign
line_item = LineItem(account)
line_item.campaign_id = campaign.id
line_item.name = 'my first ad'
line_item.product_type = PRODUCT.PROMOTED_TWEETS
line_item.placements = [PLACEMENT.ALL_ON_TWITTER]
line_item.objective = OBJECTIVE.TWEET_ENGAGEMENTS
line_item.bid_amount_local_micro = 10000
line_item.entity_status = ENTITY_STATUS.PAUSED
line_item.save()

# add targeting criteria
targeting_criteria = TargetingCriteria(account)
targeting_criteria.line_item_id = line_item.id
targeting_criteria.targeting_type = 'LOCATION'
targeting_criteria.targeting_value = '00a8b25e420adc94'
targeting_criteria.save()
