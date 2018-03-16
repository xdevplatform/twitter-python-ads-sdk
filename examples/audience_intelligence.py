from twitter_ads.client import Client
from twitter_ads.audience import AudienceIntelligence
from twitter_ads.enum import CONVERSATION_TYPE, AUDIENCE_DEFINITION

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# create a new instance of AI to get conversations
ai = AudienceIntelligence(account)
ai.targeting_inputs = [{
	  "targeting_type": 'GENDER',
	  "targeting_value": '2'
	}, {
	  "targeting_type": 'AGEBUCKET',
	  "targeting_value": 'AGE_OVER_50'
	}]
ai.conversation_type = CONVERSATION_TYPE.HASHTAG
ai.audience_definition = AUDIENCE_DEFINITION.TARGETING_CRITERIA
response = ai.conversations()
for i in range(0, response.count):
	ai = response.next()
	print ai.localized['targeting_type']
	print ai.localized['targeting_value']
	print "\n"

# create a new instance of AI to get demographics
ai = AudienceIntelligence(account)
ai.targeting_inputs =  [{
    "targeting_type": 'BROAD_MATCH_KEYWORD',
    "targeting_value": 'womensmarch2018',
    "start_time": '2017-12-31'
	}]
ai.audience_definition = AUDIENCE_DEFINITION.KEYWORD_AUDIENCE
response = ai.demographics()
for key in response.keys():
	print key
	print response[key]
	print "\n"