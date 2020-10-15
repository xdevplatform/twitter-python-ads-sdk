# analytics test
# 1. make POST stats call
# 2. poll GET call
# 3. download tar file
# 4. unzip 
import requests
import gzip
import time
import StringIO
import json
import yaml
import os


from twitter_ads import API_VERSION
from twitter_ads.client import Client
from twitter_ads.http import Request
from twitter_ads.error import Error

# read params from file
with open('async_params.json') as json_file:
	params_file = json.load(json_file)

# read .twurlrc and use defaults
with open(os.path.expanduser('~/.twurlrc'), 'r') as stream:
    twurlrc = yaml.load(stream, Loader=yaml.FullLoader)
    screen_name = twurlrc['configuration']['default_profile'][0]
    consumer_key = twurlrc['configuration']['default_profile'][1]
    profile = twurlrc['profiles'][screen_name][consumer_key]

# use twurl defaults
CONSUMER_KEY = profile['consumer_key']
CONSUMER_SECRET = profile['consumer_secret']
ACCESS_TOKEN = profile['token']
ACCESS_TOKEN_SECRET = profile['secret']
ADS_ACCOUNT         = params_file['account_id']
USER                = params_file['user']

params = params_file['params']

# initialize the twitter ads api client
client = Client(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

headers = {'X-As-User': USER}

# stats call
create_job = '/' + API_VERSION + '/stats/jobs/accounts/{account_id}'.format(account_id=ADS_ACCOUNT)

try:
    response = Request(client, 'post', create_job, params=params, headers=headers).perform()
except Error as e:
    # see twitter_ads.error for more details
    print e.details
    raise

# check job status
check_job = create_job = '/' + API_VERSION + '/stats/jobs/accounts/{account_id}'.format(account_id=ADS_ACCOUNT)
params = {
	'job_ids': response.body['data']['id_str']
}

while True:
	try:
	    response = Request(client, 'get', check_job, params=params, headers=headers).perform()
	    if response.body['data'][0]['url'] is not None:
	    	break
			
		time.sleep(15)
	except Error as e:
	    # see twitter_ads.error for more details
	    print e.details
	    raise

# download file
r = requests.get(response.body['data'][0]['url'], stream=True)
file = StringIO.StringIO(r.content)
z = gzip.GzipFile(fileobj=file)
stats_json = z.read()
print stats_json
