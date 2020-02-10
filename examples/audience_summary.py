from twitter_ads.client import Client
from twitter_ads.targeting import AudienceSummary

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# targeting criteria params
params = {
        "targeting_criteria": [
          {
            "targeting_type":"LOCATION",
            "targeting_value":"96683cc9126741d1"
          },
          {
            "targeting_type":"BROAD_KEYWORD",
            "targeting_value":"cats"
          },
          {
            "targeting_type":"SIMILAR_TO_FOLLOWERS_OF_USER",
            "targeting_value": "14230524"
          },
          {
            "targeting_type":"SIMILAR_TO_FOLLOWERS_OF_USER",
            "targeting_value": "90420314"
          }
        ]
}

audience_summary = AudienceSummary.load(account=account, params=params)

print (audience_summary.audience_size)
