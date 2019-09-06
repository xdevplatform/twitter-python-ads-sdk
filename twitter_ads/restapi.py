from twitter_ads.http import Request
from twitter_ads.resource import resource_property, Resource


class UserIdLookup(Resource):
    PROPERTIES = {}

    DOMAIN = 'https://api.twitter.com'
    RESOURCE = '/1.1/users/show.json'

    @classmethod
    def load(klass, account, screen_name):
        params = {}
        params['screen_name'] = screen_name

        response = Request(
            account.client,
            'get',
            resource=klass.RESOURCE,
            params=params,
            domain=klass.DOMAIN
        ).perform()
        return klass(account).from_response(response.body, response.headers)


# users/show endpoint properties
# read-only
resource_property(UserIdLookup, 'id', readonly=True)
resource_property(UserIdLookup, 'id_str', readonly=True)
resource_property(UserIdLookup, 'screen_name', readonly=True)
