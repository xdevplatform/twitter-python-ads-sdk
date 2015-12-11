from twitter_ads.client import Client
from twitter_ads.tweet import Tweet

CONSUMER_KEY = 'your consumer key'
CONSUMER_SECRET = 'your consumer secret'
ACCESS_TOKEN = 'access token'
ACCESS_TOKEN_SECRET = 'access token secret'
ACCOUNT_ID = 'account id'

# initialize the client
client = Client(
    CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# load the advertiser account instance
account = client.accounts().next()

# create an instance of our Tweet container
tweet = Tweet(account)

# preview an existing Tweet
tweet.get_preview(id=661845592138776576)

# preview a new Tweet
tweet.get_preview(status="Hello World!")

# preview a new Tweet with an image
tweet.get_preview(status="Hello World!", media_ids=634458428836962304)

# preview a new Tweet with multiple images (up to 4)
images = [
  634458428836962305, 634458428836962306,
  634458428836962307, 634458428836962308
]

tweet.get_preview(status="Hello World!", media_ids=images)
