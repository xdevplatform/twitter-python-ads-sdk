import json

from twitter_ads.campaign import TargetingCriteria
from twitter_ads.client import Client

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""
ADS_ACCOUNT = ""

# initialize the twitter ads api client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load up the account instance
account = client.accounts(ADS_ACCOUNT)

# load file
# assumes targeting.json is structured as follows
"""
[  
  {  
    "operation_type":"Create",
    "params":{  
      "line_item_id":"1a2bc",
      "targeting_value":"digital",
      "operator_type":"EQ",
      "targeting_type":"BROAD_KEYWORD"
    }
  },
  {  
    "operation_type":"Create",
    "params":{  
      "line_item_id":"1a2bc",
      "targeting_value":"analog",
      "operator_type":"NE",
      "targeting_type":"BROAD_KEYWORD"
    }
  }
]
"""
with open('targeting.json', 'r') as f:
    targeting_data = json.load(f)

targeting = []
for obj in targeting_data:
    tc = TargetingCriteria(account)
    tc.line_item_id = obj['params']['line_item_id']
    tc.operator_type = obj['params']['operator_type']
    tc.targeting_type = obj['params']['targeting_type']
    tc.targeting_value = obj['params']['targeting_value']
    targeting.append(tc)

TargetingCriteria.batch_save(account, targeting)
