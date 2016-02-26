# Copyright (C) 2015 Twitter, Inc.

from twitter_ads.client import Client
from twitter_ads.http import Request

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'user access token'
ACCESS_TOKEN_SECRET = 'user access token secret'
ADS_ACCOUNT = 'ads account id'

# initialize the twitter ads api client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# using the Request object you can manually call any twitter API resource including media uploads.

# note: video uploads a bit more specialized and should be done using the
# twitter_ads.http.MediaUpload class.

# upload an image to POST media/upload
resource = '/1.1/media/upload.json'
domain = 'https://upload.twitter.com'
files = {'media': (None, open('/path/to/file.jpg', 'rb'))}
response = Request(client, 'post', resource, files=files, domain=domain).perform()

# extract the media_id value from the response
media_id = response.body['media_id']
