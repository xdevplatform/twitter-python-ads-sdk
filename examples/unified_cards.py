from twitter_ads.client import Client
from twitter_ads.creative import Card
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

# fetch all
card = Card.all(account, card_ids="1502039998987587584").first

# fetch by card-id
card = Card.load(account=account, id="1502039998987587584")

# edit card destination.url
card.components= [
        {
          "media_key": "13_794652834998325248",
          "media_metadata": {
            "13_794652834998325248": {
              "type": "VIDEO",
              "url": "https://video.twimg.com/amplify_video/794652834998325248/vid/640x360/pUgE2UKcfPwF_5Uh.mp4",
              "width": 640,
              "height": 360,
              "video_duration": 7967,
              "video_aspect_ratio": "16:9"
            }
          },
          "type": "MEDIA"
        },
        {
          "title": "Twitter",
          "destination": {
            "url": "http://twitter.com/newvalue",
            "type": "WEBSITE"
          },
          "type": "DETAILS"
        }
      ]

card.save()
print(card.components)

# create new card
newcard = Card(account=account)
newcard.name="my new card"
components= [
        {
          "media_key": "13_794652834998325248",
          "media_metadata": {
            "13_794652834998325248": {
              "type": "VIDEO",
              "url": "https://video.twimg.com/amplify_video/794652834998325248/vid/640x360/pUgE2UKcfPwF_5Uh.mp4",
              "width": 640,
              "height": 360,
              "video_duration": 7967,
              "video_aspect_ratio": "16:9"
            }
          },
          "type": "MEDIA"
        },
        {
          "title": "Twitter",
          "destination": {
            "url": "http://twitter.com/login",
            "type": "WEBSITE"
          },
          "type": "DETAILS"
        }
      ]
newcard.components=components
newcard.save()
print(newcard.id)