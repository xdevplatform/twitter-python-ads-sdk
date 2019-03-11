from datetime import datetime, timedelta
from dateutil.parser import parse

from twitter_ads.campaign import LineItem
from twitter_ads.client import Client
from twitter_ads.enum import GRANULARITY, METRIC_GROUP, PLACEMENT
from twitter_ads.utils import remove_minutes


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
ACCOUNT_ID = ''

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# analytics request parameters
metric_groups = [METRIC_GROUP.ENGAGEMENT]
granularity = GRANULARITY.HOUR
placement = PLACEMENT.ALL_ON_TWITTER

# For checking the active entities endpoint for the last day
end_time = datetime.utcnow().date()
start_time = end_time - timedelta(days=1)

# Active Entities for Line Items
active_entities = LineItem.active_entities(account, start_time, end_time)

# Entity IDs to fetch analytics data for
# Note: analytics endpoints support a
# maximum of 20 entity IDs per request
ids = [d['entity_id'] for d in active_entities]

# Function for determining the start and end time
# to be used in the subsequent analytics request
def date_range(data):
    """Returns the minimum activity start time and the maximum activity end time
    from the active entities response.

    This function assumes that the subsequent analytics request will use `HOUR`
    granularity. Thus, minutes (and seconds and so on) are removed from the
    start and end times and an *hour* is added to the end time.

    These are the dates that should be used in the subsequent analytics request.
    """
    start = min([parse(d['activity_start_time']) for d in data])
    end = max([parse(d['activity_end_time']) for d in data])
    start = remove_minutes(start)
    end = remove_minutes(end) + timedelta(hours=1)
    return start, end

# Date range for analytics request
start, end = date_range(active_entities)

# Analytics request for specific Line Item IDs
# Granularity is set to `HOUR`
# Based on the activity start and end times
# only one hour of data is being requested
# which is why the arrays have a single element
LineItem.all_stats(account, ids, metric_groups, granularity=granularity, placement=placement, start_time=start, end_time=end)
"""
[
  {
    "id": "eeukx",
    "id_data": [
      {
        "metrics": {
          "app_clicks": None,
          "card_engagements": None,
          "carousel_swipes": None,
          "clicks": [
            71
          ],
          "engagements": [
            141
          ],
          "follows": [
            2
          ],
          "impressions": [
            3613
          ],
          "likes": [
            14
          ],
          "poll_card_vote": None,
          "qualified_impressions": None,
          "replies": [
            1
          ],
          "retweets": None,
          "tweets_send": [
            1
          ],
          "unfollows": None,
          "url_clicks": [
            1
          ]
        },
        "segment": None
      }
    ]
  },
  {
    "id": "eeulb",
    "id_data": [
      {
        "metrics": {
          "app_clicks": None,
          "card_engagements": None,
          "carousel_swipes": None,
          "clicks": [
            75
          ],
          "engagements": [
            297
          ],
          "follows": None,
          "impressions": [
            2020
          ],
          "likes": [
            16
          ],
          "poll_card_vote": None,
          "qualified_impressions": None,
          "replies": None,
          "retweets": [
            2
          ],
          "tweets_send": None,
          "unfollows": None,
          "url_clicks": [
            2
          ]
        },
        "segment": None
      }
    ]
  }
]
"""
