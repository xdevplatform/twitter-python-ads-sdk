from twitter_ads.enum import TRANSFORM
from twitter_ads.resource import resource_property, Resource, Persistence, Batch, Analytics
from twitter_ads.http import Request
from twitter_ads.cursor import Cursor

class Pixel(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/1/accounts/{account_id}/web_event_tags'
    RESOURCE = '/1/accounts/{account_id}/web_event_tags/{id}'

# read only
resource_property(Pixel, 'embed_code', readonly=True)
resource_property(Pixel, 'id', readonly=True)
resource_property(Pixel, 'status', readonly=True)
resource_property(Pixel, 'website_tag_id', readonly=True)

#writeable
resource_property(Pixel, 'account_id')
resource_property(Pixel, 'name')
resource_property(Pixel, 'click_window')
resource_property(Pixel, 'view_through_window')
resource_property(Pixel, 'type')
resource_property(Pixel, 'retargeting_enabled')
