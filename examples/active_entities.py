from datetime import datetime, timedelta
from dateutil.parser import parse

from twitter_ads.campaign import LineItem
from twitter_ads.client import Client
from twitter_ads.enum import GRANULARITY, METRIC_GROUP, PLACEMENT
from twitter_ads.utils import remove_hours


CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# analytics request parameters
metric_groups = [METRIC_GROUP.ENGAGEMENT]
granularity = GRANULARITY.HOUR
placement = PLACEMENT.ALL_ON_TWITTER

# for checking the active entities endpoint for the last day
end_time = datetime.utcnow().date()
start_time = end_time - timedelta(days=1)

# active entities for line items
active_entities = LineItem.active_entities(account, start_time, end_time)

# entity IDs to fetch analytics data for
# note: analytics endpoints support a
# maximum of 20 entity IDs per request
ids = [d['entity_id'] for d in active_entities]

# function for determining the start and end time
# to be used in the subsequent analytics request
# note: if `active_entities` is empty, `date_range` will error
def date_range(data):
    """Returns the minimum activity start time and the maximum activity end time
    from the active entities response. These dates are modified in the following
    way. The hours (and minutes and so on) are removed from the start and end
    times and a *day* is added to the end time. These are the dates that should
    be used in the subsequent analytics request.
    """
    start = min([parse(d['activity_start_time']) for d in data])
    end = max([parse(d['activity_end_time']) for d in data])
    start = remove_hours(start)
    end = remove_hours(end) + timedelta(days=1)
    return start, end

# date range for analytics request
start, end = date_range(active_entities)

# the analytics request for specific line item IDs
# using the derived start and end times
# from the active entities response with
# granularity is set to `HOUR`
LineItem.all_stats(account, ids, metric_groups, granularity=granularity, placement=placement, start_time=start, end_time=end)
"""
[
  {
    "id": "du549",
    "id_data": [
      {
        "metrics": {
          "app_clicks": None,
          "card_engagements": None,
          "carousel_swipes": None,
          "clicks": [
            0,32,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          "engagements": [
            0,79,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          "follows": None,
          "impressions": [
            0,2195,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          "likes": [
            0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          "poll_card_vote": None,
          "qualified_impressions": None,
          "replies": None,
          "retweets": None,
          "tweets_send": None,
          "unfollows": None,
          "url_clicks": [
            0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ]
        },
        "segment": None
      }
    ]
  },
  {
    "id": "du5o5",
    "id_data": [
      {
        "metrics": {
          "app_clicks": None,
          "card_engagements": None,
          "carousel_swipes": None,
          "clicks": [
            0,1,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          "engagements": [
            0,2,29,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          "follows": None,
          "impressions": [
            0,14,538,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          "likes": [
            0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
          ],
          "poll_card_vote": None,
          "qualified_impressions": None,
          "replies": None,
          "retweets": None,
          "tweets_send": None,
          "unfollows": None,
          "url_clicks": None
        },
        "segment": None
      }
    ]
  }
]
"""
