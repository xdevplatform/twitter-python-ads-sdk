from datetime import datetime

from twitter_ads.client import Client
from twitter_ads.campaign import Campaign, LineItem, TargetingCriteria
from twitter_ads.enum import ENTITY_STATUS, OBJECTIVE, PLACEMENT, PRODUCT

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'user access token'
ACCESS_TOKEN_SECRET = 'user access token secret'
ADS_ACCOUNT = 'ads account id'

# initialize the twitter ads api client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load up the account instance
account = client.accounts(ADS_ACCOUNT)

# create two campaigns
campaign_1 = Campaign(account)
campaign_1.funding_instrument_id = account.funding_instruments().next().id
campaign_1.daily_budget_amount_local_micro = 1000000
campaign_1.name = 'my first campaign'
campaign_1.entity_status = ENTITY_STATUS.PAUSED
campaign_1.start_time = datetime.utcnow()

campaign_2 = Campaign(account)
campaign_2.funding_instrument_id = account.funding_instruments().next().id
campaign_2.daily_budget_amount_local_micro = 2000000
campaign_2.name = 'my second campaign'
campaign_2.entity_status = ENTITY_STATUS.PAUSED
campaign_2.start_time = datetime.utcnow()

campaigns_list = [campaign_1, campaign_2]
Campaign.batch_save(account, campaigns_list)

# modify the created campaigns
campaign_1.name = 'my modified first campaign'
campaign_2.name = 'my modified second campaign'

Campaign.batch_save(account, campaigns_list)

# create line items for campaign_1
line_item_1 = LineItem(account)
line_item_1.campaign_id = campaign_1.id
line_item_1.name = 'my first ad'
line_item_1.product_type = PRODUCT.PROMOTED_TWEETS
line_item_1.placements = [PLACEMENT.ALL_ON_TWITTER]
line_item_1.objective = OBJECTIVE.TWEET_ENGAGEMENTS
line_item_1.bid_amount_local_micro = 10000
line_item_1.entity_status = ENTITY_STATUS.PAUSED

line_item_2 = LineItem(account)
line_item_2.campaign_id = campaign_1.id
line_item_2.name = 'my second ad'
line_item_2.product_type = PRODUCT.PROMOTED_TWEETS
line_item_2.placements = [PLACEMENT.ALL_ON_TWITTER]
line_item_2.objective = OBJECTIVE.TWEET_ENGAGEMENTS
line_item_2.bid_amount_local_micro = 20000
line_item_2.entity_status = ENTITY_STATUS.PAUSED

line_items_list = [line_item_1, line_item_2]
LineItem.batch_save(account, line_items_list)

# create targeting criteria for line_item_1
targeting_criterion_1 = TargetingCriteria(account)
targeting_criterion_1.line_item_id = line_item_1.id
targeting_criterion_1.targeting_type = 'LOCATION'
targeting_criterion_1.targeting_value = '00a8b25e420adc94'

targeting_criterion_2 = TargetingCriteria(account)
targeting_criterion_2.line_item_id = line_item_1.id
targeting_criterion_2.targeting_type = 'PHRASE_KEYWORD'
targeting_criterion_2.targeting_value = 'righteous dude'

targeting_criteria_list = [targeting_criterion_1, targeting_criterion_2]
TargetingCriteria.batch_save(account, targeting_criteria_list)

targeting_criterion_1.to_delete = True
targeting_criterion_2.to_delete = True

TargetingCriteria.batch_save(account, targeting_criteria_list)

line_item_1.to_delete = True
line_item_2.to_delete = True

LineItem.batch_save(account, line_items_list)

campaign_1.to_delete = True
campaign_2.to_delete = True

Campaign.batch_save(account, campaigns_list)
