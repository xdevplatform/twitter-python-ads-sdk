from twitter_ads.client import Client
from twitter_ads.creative import MediaLibrary
from twitter_ads.enum import MEDIA_CATEGORY
from twitter_ads.http import Request


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN = ''
ACCESS_TOKEN_SECRET = ''
ACCOUNT_ID = ''

# initialize the client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts(ACCOUNT_ID)

# upload an image to POST media/upload
resource = '/1.1/media/upload.json'
domain = 'https://upload.twitter.com'
files = {'media': (None, open('/path/to/file.jpg', 'rb'))}
response = Request(client, 'post', resource, files=files, domain=domain).perform()
media_id = response.body['media_id']

# add to media library
media_library = MediaLibrary(account)
media_library.name = 'name'
media_library.file_name = 'name.jpeg'
media_library.media_id = media_id
media_library.media_category = MEDIA_CATEGORY.TWEET_IMAGE
media_library.save()
