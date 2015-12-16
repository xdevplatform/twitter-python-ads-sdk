# Copyright (C) 2015 Twitter, Inc.

"""Container for all creative management logic used by the Ads API SDK."""

from twitter_ads.enum import TRANSFORM
from twitter_ads.resource import resource_property, Resource, Persistence, Analytics
from twitter_ads.http import Request


class PromotedAccount(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/promoted_accounts'
    RESOURCE_STATS = '/0/stats/accounts/{account_id}/promoted_accounts'
    RESOURCE = '/0/accounts/{account_id}/promoted_accounts/{id}'

# promoted account properties
# read-only
resource_property(PromotedAccount, 'id', readonly=True)
resource_property(PromotedAccount, 'approval_status', readonly=True)
resource_property(PromotedAccount, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(PromotedAccount, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(PromotedAccount, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(PromotedAccount, 'line_item_id')
resource_property(PromotedAccount, 'user_id')
resource_property(PromotedAccount, 'paused', transform=TRANSFORM.BOOL)


class PromotedTweet(Resource, Persistence, Analytics):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/promoted_tweets'
    RESOURCE_STATS = '/0/stats/accounts/{account_id}/promoted_tweets'
    RESOURCE = '/0/accounts/{account_id}/promoted_tweets/{id}'

    def save(self):
        """
        Saves or updates the current object instance depending on the
        presence of `object.id`.
        """
        if self.id:
            method = 'put'
            resource = self.RESOURCE.format(account_id=self.account.id, id=self.id)
        else:
            method = 'post'
            resource = self.RESOURCE_COLLECTION.format(account_id=self.account.id)

        params = self.to_params()
        if 'tweet_id' in params:
            params['tweet_ids'] = [params['tweet_id']]
            del params['tweet_id']

        response = Request(
            self.account.client, method,
            resource, params=params).perform()

        self.from_response(response.body['data'])

# promoted tweet properties
# read-only
resource_property(PromotedTweet, 'id', readonly=True)
resource_property(PromotedTweet, 'approval_status', readonly=True)
resource_property(PromotedTweet, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(PromotedTweet, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(PromotedTweet, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(PromotedTweet, 'line_item_id')
resource_property(PromotedTweet, 'tweet_id')
resource_property(PromotedTweet, 'paused', transform=TRANSFORM.BOOL)


class Video(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/videos'
    RESOURCE = '/0/accounts/{account_id}/videos/{id}'

# video properties
# read-only
resource_property(Video, 'id', readonly=True)
resource_property(Video, 'tweeted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(Video, 'ready_to_tweet', readonly=True, transform=TRANSFORM.BOOL)
resource_property(Video, 'duration', readonly=True)
resource_property(Video, 'reasons_not_servable', readonly=True)
resource_property(Video, 'preview_url', readonly=True)
resource_property(Video, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(Video, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(Video, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(Video, 'title')
resource_property(Video, 'description')
resource_property(Video, 'video_media_id')


class WebsiteCard(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/website'
    RESOURCE = '/0/accounts/{account_id}/cards/website/{id}'

# website card properties
# read-only
resource_property(WebsiteCard, 'id', readonly=True)
resource_property(WebsiteCard, 'preview_url', readonly=True)
resource_property(WebsiteCard, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(WebsiteCard, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(WebsiteCard, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(WebsiteCard, 'name')
resource_property(WebsiteCard, 'website_title')
resource_property(WebsiteCard, 'website_url')
resource_property(WebsiteCard, 'website_cta')
resource_property(WebsiteCard, 'image_media_id')


class LeadGenCard(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/lead_gen'
    RESOURCE = '/0/accounts/{account_id}/cards/lead_gen/{id}'

# lead gen card properties
# read-only
resource_property(LeadGenCard, 'id', readonly=True)
resource_property(LeadGenCard, 'preview_url', readonly=True)
resource_property(LeadGenCard, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(LeadGenCard, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(LeadGenCard, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(LeadGenCard, 'name')
resource_property(LeadGenCard, 'image_media_id')
resource_property(LeadGenCard, 'cta')
resource_property(LeadGenCard, 'fallback_url')
resource_property(LeadGenCard, 'privacy_policy_url')
resource_property(LeadGenCard, 'title')
resource_property(LeadGenCard, 'submit_url')
resource_property(LeadGenCard, 'submit_method')
resource_property(LeadGenCard, 'custom_destination_url')
resource_property(LeadGenCard, 'custom_destination_text')
resource_property(LeadGenCard, 'custom_key_screen_name')
resource_property(LeadGenCard, 'custom_key_name')
resource_property(LeadGenCard, 'custom_key_email')


class AppDownloadCard(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/app_download'
    RESOURCE = '/0/accounts/{account_id}/cards/app_download/{id}'

# app download card properties
# read-only
resource_property(AppDownloadCard, 'id', readonly=True)
resource_property(AppDownloadCard, 'preview_url', readonly=True)
resource_property(AppDownloadCard, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(AppDownloadCard, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(AppDownloadCard, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(AppDownloadCard, 'name')
resource_property(AppDownloadCard, 'app_country_code')
resource_property(AppDownloadCard, 'iphone_app_id')
resource_property(AppDownloadCard, 'iphone_deep_link')
resource_property(AppDownloadCard, 'ipad_app_id')
resource_property(AppDownloadCard, 'ipad_deep_link')
resource_property(AppDownloadCard, 'googleplay_app_id')
resource_property(AppDownloadCard, 'googleplay_deep_link')
resource_property(AppDownloadCard, 'app_cta')
resource_property(AppDownloadCard, 'custom_icon_media_id')
resource_property(AppDownloadCard, 'custom_app_description')


class ImageAppDownloadCard(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/image_app_download'
    RESOURCE = '/0/accounts/{account_id}/cards/image_app_download/{id}'

# image app download card properties
# read-only
resource_property(ImageAppDownloadCard, 'id', readonly=True)
resource_property(ImageAppDownloadCard, 'preview_url', readonly=True)
resource_property(ImageAppDownloadCard, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(ImageAppDownloadCard, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(ImageAppDownloadCard, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(ImageAppDownloadCard, 'name')
resource_property(ImageAppDownloadCard, 'app_country_code')
resource_property(ImageAppDownloadCard, 'iphone_app_id')
resource_property(ImageAppDownloadCard, 'iphone_deep_link')
resource_property(ImageAppDownloadCard, 'ipad_app_id')
resource_property(ImageAppDownloadCard, 'ipad_deep_link')
resource_property(ImageAppDownloadCard, 'googleplay_app_id')
resource_property(ImageAppDownloadCard, 'googleplay_deep_link')
resource_property(ImageAppDownloadCard, 'app_cta')
resource_property(ImageAppDownloadCard, 'wide_app_image_media_id')


class VideoAppDownloadCard(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/video_app_download'
    RESOURCE = '/0/accounts/{account_id}/cards/video_app_download/{id}'

# video app download card properties
# read-only
resource_property(VideoAppDownloadCard, 'id', readonly=True)
resource_property(VideoAppDownloadCard, 'preview_url', readonly=True)
resource_property(VideoAppDownloadCard, 'video_url', readonly=True)
resource_property(VideoAppDownloadCard, 'video_poster_url', readonly=True)
resource_property(VideoAppDownloadCard, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(VideoAppDownloadCard, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(VideoAppDownloadCard, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(VideoAppDownloadCard, 'name')
resource_property(VideoAppDownloadCard, 'app_country_code')
resource_property(VideoAppDownloadCard, 'iphone_app_id')
resource_property(VideoAppDownloadCard, 'iphone_deep_link')
resource_property(VideoAppDownloadCard, 'ipad_app_id')
resource_property(VideoAppDownloadCard, 'ipad_deep_link')
resource_property(VideoAppDownloadCard, 'googleplay_app_id')
resource_property(VideoAppDownloadCard, 'googleplay_deep_link')
resource_property(VideoAppDownloadCard, 'app_cta')
resource_property(VideoAppDownloadCard, 'image_media_id')
resource_property(VideoAppDownloadCard, 'video_id')


class ImageConversationCard(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/image_conversation'
    RESOURCE = '/0/accounts/{account_id}/cards/image_conversation/{id}'

# image conversation card properties
# read-only
resource_property(ImageConversationCard, 'id', readonly=True)
resource_property(ImageConversationCard, 'preview_url', readonly=True)
resource_property(ImageConversationCard, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(ImageConversationCard, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(ImageConversationCard, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(ImageConversationCard, 'name')
resource_property(ImageConversationCard, 'title')
resource_property(ImageConversationCard, 'first_cta')
resource_property(ImageConversationCard, 'first_cta_tweet')
resource_property(ImageConversationCard, 'second_cta')
resource_property(ImageConversationCard, 'second_cta_tweet')
resource_property(ImageConversationCard, 'thank_you_text')
resource_property(ImageConversationCard, 'thank_you_url')
resource_property(ImageConversationCard, 'image_media_id')


class VideoConversationCard(Resource, Persistence):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/cards/video_conversation'
    RESOURCE = '/0/accounts/{account_id}/cards/video_conversation/{id}'

# video conversation card properties
# read-only
resource_property(VideoConversationCard, 'id', readonly=True)
resource_property(VideoConversationCard, 'preview_url', readonly=True)
resource_property(VideoConversationCard, 'video_url', readonly=True)
resource_property(VideoConversationCard, 'video_poster_url', readonly=True)
resource_property(VideoConversationCard, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(VideoConversationCard, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(VideoConversationCard, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
# writable
resource_property(VideoConversationCard, 'name')
resource_property(VideoConversationCard, 'title')
resource_property(VideoConversationCard, 'first_cta')
resource_property(VideoConversationCard, 'first_cta_tweet')
resource_property(VideoConversationCard, 'second_cta')
resource_property(VideoConversationCard, 'second_cta_tweet')
resource_property(VideoConversationCard, 'thank_you_text')
resource_property(VideoConversationCard, 'thank_you_url')
resource_property(VideoConversationCard, 'image_media_id')
resource_property(VideoConversationCard, 'video_id')
