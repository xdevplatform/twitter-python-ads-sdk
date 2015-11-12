# Copyright (C) 2015 Twitter, Inc.

"""Container for all creative management logic used by the Ads API SDK."""

from twitter_ads.resource import resource, Resource, Persistence, Analytics


@resource
class PromotedAccount(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'approval_status': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        'deleted': {'readonly': True},
        # writable
        'line_item_id': {},
        'user_id': {},
        'paused': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/promoted_accounts'
    RESOURCE_STATS = '/0/stats/accounts/{account_id}/promoted_accounts'
    RESOURCE = '/0/accounts/{account_id}/promoted_accounts/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class PromotedTweet(Resource, Persistence, Analytics):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'approval_status': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        'deleted': {'readonly': True},
        # writable
        'line_item_id': {},
        'tweet_id': {},
        'paused': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/promoted_tweets'
    RESOURCE_STATS = '/0/stats/accounts/{account_id}/promoted_tweets'
    RESOURCE = '/0/accounts/{account_id}/promoted_tweets/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class Video(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'tweeted': {'readonly': True},
        'ready_to_tweet': {'readonly': True},
        'duration': {'readonly': True},
        'reasons_not_servable': {'readonly': True},
        'preview_url': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        'deleted': {'readonly': True},
        # writable
        'title': {},
        'description': {},
        'video_media_id': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/videos'
    RESOURCE = '/0/accounts/{account_id}/videos/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class WebsiteCard(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'preview_url': {'readonly': True},
        'deleted': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        # writable
        'name': {},
        'website_title': {},
        'website_url': {},
        'website_cta': {},
        'image_media_id': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/website'
    RESOURCE = '/0/accounts/{account_id}/cards/website/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class LeadGenCard(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'preview_url': {'readonly': True},
        'deleted': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        # writable
        'name': {},
        'image_media_id': {},
        'cta': {},
        'fallback_url': {},
        'privacy_policy_url': {},
        'title': {},
        'submit_url': {},
        'submit_method': {},
        'custom_destination_url': {},
        'custom_destination_text': {},
        'custom_key_screen_name': {},
        'custom_key_name': {},
        'custom_key_email': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/lead_gen'
    RESOURCE = '/0/accounts/{account_id}/cards/lead_gen/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class AppDownloadCard(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'preview_url': {'readonly': True},
        'deleted': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        # writable
        'name': {},
        'app_country_code': {},
        'iphone_app_id': {},
        'iphone_deep_link': {},
        'ipad_app_id': {},
        'ipad_deep_link': {},
        'googleplay_app_id': {},
        'googleplay_deep_link': {},
        'app_cta': {},
        'custom_icon_media_id': {},
        'custom_app_description': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/app_download'
    RESOURCE = '/0/accounts/{account_id}/cards/app_download/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class ImageAppDownloadCard(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'preview_url': {'readonly': True},
        'deleted': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        # writable
        'name': {},
        'app_country_code': {},
        'iphone_app_id': {},
        'iphone_deep_link': {},
        'ipad_app_id': {},
        'ipad_deep_link': {},
        'googleplay_app_id': {},
        'googleplay_deep_link': {},
        'app_cta': {},
        'wide_app_image_media_id': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/image_app_download'
    RESOURCE = '/0/accounts/{account_id}/cards/image_app_download/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class VideoAppDownloadCard(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'preview_url': {'readonly': True},
        'video_url': {'readonly': True},
        'video_poster_url': {'readonly': True},
        'deleted': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        # writable
        'name': {},
        'app_country_code': {},
        'iphone_app_id': {},
        'iphone_deep_link': {},
        'ipad_app_id': {},
        'ipad_deep_link': {},
        'googleplay_app_id': {},
        'googleplay_deep_link': {},
        'app_cta': {},
        'image_media_id': {},
        'video_id': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/video_app_download'
    RESOURCE = '/0/accounts/{account_id}/cards/video_app_download/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class ImageConversationCard(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'preview_url': {'readonly': True},
        'image': {'readonly': True},
        'deleted': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        # writable
        'name': {},
        'title': {},
        'first_cta': {},
        'first_cta_tweet': {},
        'second_cta': {},
        'second_cta_tweet': {},
        'thank_you_text': {},
        'thank_you_url': {},
        'image_media_id': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/image_conversation'
    RESOURCE = '/0/accounts/{account_id}/cards/image_conversation/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account


@resource
class VideoConversationCard(Resource, Persistence):

    PROPERTIES = {
        # read-only
        'id': {'readonly': True},
        'preview_url': {'readonly': True},
        'video_url': {'readonly': True},
        'video_poster_url': {'readonly': True},
        'image': {'readonly': True},
        'deleted': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        # writable
        'name': {},
        'title': {},
        'first_cta': {},
        'first_cta_tweet': {},
        'second_cta': {},
        'second_cta_tweet': {},
        'thank_you_text': {},
        'thank_you_url': {},
        'image_media_id': {},
        'video_id': {}
    }

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/video_conversation'
    RESOURCE = '/0/accounts/{account_id}/cards/video_conversation/{id}'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account
