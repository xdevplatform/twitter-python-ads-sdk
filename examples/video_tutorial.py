from twitter_ads.client import Client
from twitter_ads.enum import CREATIVE_TYPE, ENTITY_STATUS, OBJECTIVE, PRODUCT
from twitter_ads.campaign import Campaign, LineItem
from twitter_ads.creative import AccountMedia, Video
from twitter_ads import API_VERSION

from datetime import datetime

from twython import Twython, TwythonError

# auth
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

# the video to be uploaded
video = open('/path/to/sample-video.mp4', 'rb')

upload_video = twitter.upload_video(media=video, media_type='video/mp4', media_category='amplify_video', check_progress=True)

#grab the media_id from the response
media_id = upload_video['media_id']

client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

account = client.accounts(ADS_ACCOUNT)

video = Video(account)
video.video_media_id = media_id # from previous step
video.description = "My sample videos"
video.title = "Video tutorial test"
video.save()

#grab the video_id from the response
video_id = video.id
print video_id

account_media = AccountMedia(account)
account_media.video_id = video_id
account_media.creative_type = CREATIVE_TYPE.PREROLL
account_media.save()

# create a campaign
campaign = Campaign(account)
campaign.name="Video tutorial test"
# get the first funding instrument on the account
campaign.funding_instrument_id = account.funding_instruments().first.id
campaign.daily_budget_amount_local_micro = 1000000000
campaign.entity_status = ENTITY_STATUS.PAUSED
campaign.start_time = datetime.utcnow()
campaign.save()

# create a line item with the VIDEO_VIEWS_PREROLL
# objective and product_type MEDIA
line_item = LineItem(account)
line_item.objective = OBJECTIVE.VIDEO_VIEWS_PREROLL

line_item.campaign_id = campaign.id
line_item.name = 'Video tutorial example'
line_item.product_type = 'MEDIA'
line_item.placements = [PLACEMENT.ALL_ON_TWITTER]
line_item.bid_amount_local_micro = 1000000
line_item.entity_status = ENTITY_STATUS.PAUSED
line_item.categories = 'IAB1'
line_item.save()

from twitter_ads.http import Request

resource = '/' + API_VERSION + '/accounts/18ce54bgxky/preroll_call_to_actions'.format(account_id=account.id)
params = { 
    'line_item_id' : line_item.id,
    'call_to_action' : 'WATCH_NOW',
    'call_to_action_url' : 'https://www.my-cta-url.com'
}

# try, build and execute the request with error handling
try:
    response = Request(client, 'post', resource, params=params).perform()
except Error as e:
    # see twitter_ads.error for more details
    print e.details
    raise

resource = '/' + API_VERSION + '/batch/accounts/18ce54bgxky/targeting_criteria'.format(account_id=account.id)

params = [
  {
    "operation_type": "Create",
    "params": {
      "line_item_id": line_item.id,
      "targeting_type": "CONTENT_PUBLISHER_USER",
      "targeting_value": "312226591",
      "negated": true
    }
  },
  {
    "operation_type": "Create",
    "params": {
      "line_item_id": line_item.id,
      "targeting_type": "IAB_CATEGORY",
      "targeting_value": "IAB2",
      "negated": true
    }
  }
]

try:
    response = Request(client, 'post', resource, params=params).perform()
except Error as e:
    # see twitter_ads.error for more details
    print e.details
    raise

# unpause the campaign
campaign.entity_status = ENTITY_STATUS.ACTIVE
campaign.save()
