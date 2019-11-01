# Copyright (C) 2015 Twitter, Inc.

"""Container for all plugable resource object logic used by the Ads API SDK."""

from datetime import datetime, timedelta
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from twitter_ads.utils import to_time, validate_whole_hours
from twitter_ads.enum import ENTITY, GRANULARITY, PLACEMENT, TRANSFORM
from twitter_ads.http import Request
from twitter_ads.cursor import Cursor
from twitter_ads.resource import Resource, resource_property
from twitter_ads import API_VERSION
from twitter_ads.utils import FlattenParams


class Analytics(Resource):
    """
    Container for all analytics related logic used by API resource objects.
    """
    PROPERTIES = {}

    ANALYTICS_MAP = {
        'Campaign': ENTITY.CAMPAIGN,
        'FundingInstrument': ENTITY.FUNDING_INSTRUMENT,
        'LineItem': ENTITY.LINE_ITEM,
        'MediaCreative': ENTITY.MEDIA_CREATIVE,
        'OrganicTweet': ENTITY.ORGANIC_TWEET,
        'PromotedTweet': ENTITY.PROMOTED_TWEET,
        'PromotedAccount': ENTITY.PROMOTED_ACCOUNT
    }

    RESOURCE_SYNC = '/' + API_VERSION + '/stats/accounts/{account_id}'
    RESOURCE_ASYNC = '/' + API_VERSION + '/stats/jobs/accounts/{account_id}'
    RESOURCE_ACTIVE_ENTITIES = '/' + API_VERSION + '/stats/accounts/{account_id}/active_entities'

    def stats(self, metrics, **kwargs):  # noqa
        """
        Pulls a list of metrics for the current object instance.
        """
        return self.__class__.all_stats(self.account, [self.id], metrics, **kwargs)

    @classmethod
    def _standard_params(klass, ids, metric_groups, **kwargs):
        """
        Sets the standard params for a stats request
        """
        end_time = kwargs.get('end_time', datetime.utcnow())
        start_time = kwargs.get('start_time', end_time - timedelta(seconds=604800))
        granularity = kwargs.get('granularity', GRANULARITY.HOUR)
        placement = kwargs.get('placement', PLACEMENT.ALL_ON_TWITTER)
        entity = kwargs.get('entity', None)

        params = {
            'metric_groups': ','.join(map(str, metric_groups)),
            'start_time': to_time(start_time, granularity),
            'end_time': to_time(end_time, granularity),
            'granularity': granularity.upper(),
            'entity': entity or klass.ANALYTICS_MAP[klass.__name__],
            'placement': placement
        }

        params['entity_ids'] = ','.join(map(str, ids))

        return params

    @classmethod
    def all_stats(klass, account, ids, metric_groups, **kwargs):
        """
        Pulls a list of metrics for a specified set of object IDs.
        """
        params = klass._standard_params(ids, metric_groups, **kwargs)

        resource = klass.RESOURCE_SYNC.format(account_id=account.id)
        response = Request(account.client, 'get', resource, params=params).perform()
        return response.body['data']

    @classmethod
    def queue_async_stats_job(klass, account, ids, metric_groups, **kwargs):
        """
        Queues a list of metrics for a specified set of object IDs asynchronously
        """
        params = klass._standard_params(ids, metric_groups, **kwargs)

        params['platform'] = kwargs.get('platform', None)
        params['country'] = kwargs.get('country', None)
        params['segmentation_type'] = kwargs.get('segmentation_type', None)

        resource = klass.RESOURCE_ASYNC.format(account_id=account.id)
        response = Request(account.client, 'post', resource, params=params).perform()
        return Analytics(account).from_response(response.body['data'], headers=response.headers)

    @classmethod
    @FlattenParams
    def async_stats_job_result(klass, account, **kwargs):
        """
        Returns the results of the specified async job IDs
        """
        resource = klass.RESOURCE_ASYNC.format(account_id=account.id)
        request = Request(account.client, 'get', resource, params=kwargs)

        return Cursor(Analytics, request, init_with=[account])

    @classmethod
    def async_stats_job_data(klass, account, url, **kwargs):
        """
        Returns the results of the specified async job IDs
        """
        resource = urlparse(url)
        domain = '{0}://{1}'.format(resource.scheme, resource.netloc)

        response = Request(account.client, 'get', resource.path, domain=domain,
                           raw_body=True, stream=True).perform()

        return response.body

    @classmethod
    @FlattenParams
    def active_entities(klass, account, start_time, end_time, **kwargs):
        """
        Returns the details about which entities' analytics metrics
        have changed in a given time period.
        """
        entity = kwargs.get('entity') or klass.ANALYTICS_MAP[klass.__name__]
        if entity == klass.ANALYTICS_MAP['OrganicTweet']:
            raise ValueError("'OrganicTweet' not support with 'active_entities'")

        # The start and end times must be expressed in whole hours
        validate_whole_hours(start_time)
        validate_whole_hours(end_time)

        params = {
            'entity': entity,
            'start_time': to_time(start_time, None),
            'end_time': to_time(end_time, None)
        }
        params.update(kwargs)

        resource = klass.RESOURCE_ACTIVE_ENTITIES.format(account_id=account.id)
        response = Request(account.client, 'get', resource, params=params).perform()
        return response.body['data']


# Analytics properties
# read-only
resource_property(Analytics, 'id', readonly=True)
resource_property(Analytics, 'id_str', readonly=True)
resource_property(Analytics, 'status', readonly=True)
resource_property(Analytics, 'url', readonly=True)
resource_property(Analytics, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(Analytics, 'expires_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(Analytics, 'updated_at', readonly=True, transform=TRANSFORM.TIME)

resource_property(Analytics, 'start_time', readonly=True, transform=TRANSFORM.TIME)
resource_property(Analytics, 'end_time', readonly=True, transform=TRANSFORM.TIME)
resource_property(Analytics, 'entity', readonly=True)
resource_property(Analytics, 'entity_ids', readonly=True)
resource_property(Analytics, 'placement', readonly=True)
resource_property(Analytics, 'granularity', readonly=True)
resource_property(Analytics, 'metric_groups', readonly=True)
