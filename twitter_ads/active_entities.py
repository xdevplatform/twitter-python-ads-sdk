# Copyright (C) 2019 Twitter, Inc.

"""Container for all active entities logic used by the Ads API SDK."""

from twitter_ads.enum import TRANSFORM
from twitter_ads.resource import resource_property, Resource


class ActiveEntities(Resource):

    PROPERTIES = {}

    # TODO: use `API_VERSION`
    RESOURCE_COLLECTION = '/5/stats/accounts/{account_id}/active_entities'

    def load(klass):
        raise AttributeError("'ActiveEntities' object has no attribute 'load'")

    def reload(klass):
        raise AttributeError("'ActiveEntities' object has no attribute 'reload'")

# active entities properties
# read-only
resource_property(ActiveEntities, 'entity_id', readonly=True)
resource_property(ActiveEntities, 'activity_start_time', readonly=True, transform=TRANSFORM.TIME)
resource_property(ActiveEntities, 'activity_end_time', readonly=True, transform=TRANSFORM.TIME)
