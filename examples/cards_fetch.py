from twitter_ads.client import Client
from twitter_ads.creative import CardsFetch
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

# retrieve a Tweet
tweet_id = '973002610033610753' # use one of your own Tweets
resource = '/1.1/statuses/show/{id}.json'.format(id=tweet_id)
domain = 'https://api.twitter.com'
params = {'include_card_uri' : 'true'}
response = Request(client, 'get', resource, domain=domain, params=params).perform()
card_uri = response.body['card_uri'] # Tweet must include a card_uri card

# fetch by card_uri
cf = CardsFetch(account)
card = cf.load(account, card_uri=card_uri)
card.card_type # 'VIDEO_POLLS'
card.id # '5g83p'

# fetch by card id
same_card = cf.load(account, card_id=card.id)
same_card.card_type # 'VIDEO_POLLS'
same_card.card_uri # 'card://973002559269974016'
