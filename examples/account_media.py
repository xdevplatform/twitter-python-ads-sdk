# Copyright (C) 2015-2016 Twitter, Inc.
# Note: All account_media/media_creatives must be uploaded via the media-upload endpoints
# See: https://dev.twitter.com/rest/media/uploading-media

from twitter_ads.client import Client
from twitter_ads.http import Request
from twitter_ads.enums import CREATIVE_TYPE
from twitter_ads.creative import AccountMedia, MediaCreative

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# grab the first line_item on the account
line_item_id = account.line_items().first.id

# retrive the `id` of the media creative associated with a line item
print account.media_creatives().first.id

# retrieve the `id` of the first account media associated with the account
account_media_id = account.account_media().first.id

# create a new account media
account_media = AccountMedia(account)
account_media.media_id = 'your-media-id' 
# OR account_media.video_id OR account_media.vast_url
# see the media_upload.py example for more details
account_media.creative_type = CREATIVE_TYPE.BANNER
account_media.save()


#create a new media creative
media_creative = MediaCreative(account)
media_creative.line_item_id = line_item_id
media_creative.account_media_id = account_media_id
media_creative.landing_url = "https://my-landing-url"
media_creative.save()

# delete the media creative
media_creative.delete()
