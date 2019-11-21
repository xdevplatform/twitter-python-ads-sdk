from twitter_ads.client import Client
from twitter_ads.creative import MediaLibrary
from twitter_ads.enum import MEDIA_CATEGORY
from twitter_ads.http import Request


CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'user access token'
ACCESS_TOKEN_SECRET = 'user access token secret'
ACCOUNT_ID = 'ads account id'

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# upload an image to POST media/upload
# https://developer.twitter.com/en/docs/ads/creatives/guides/media-library
resource = '/1.1/media/upload.json'
params = {
    'additional_owners': '756201191646691328',
    'media_category': MEDIA_CATEGORY.TWEET_IMAGE
}
domain = 'https://upload.twitter.com'
files = {'media': (None, open('/path/to/file.jpg', 'rb'))}
response = Request(client, 'post', resource, files=files, domain=domain, params=params).perform()
media_key = response.body['media_key']

# add to media library
media_library = MediaLibrary(account)
media_library.name = 'name'
media_library.file_name = 'name.png'
media_library.media_key = media_key
data = media_library.add()

# update the media
data.name = 'name - updated'
data.update()
