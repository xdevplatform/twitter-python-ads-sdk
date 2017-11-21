import pytest
import responses
import unittest

from tests.support import with_resource, with_fixture, characters

from twitter_ads.account import Account
from twitter_ads.campaign import Campaign
from twitter_ads.client import Client
from twitter_ads.cursor import Cursor
from twitter_ads import API_VERSION


class TestCampaigns(unittest.TestCase):
    @responses.activate
    def setUp(cls):
        # Test account response
        responses.add(
                responses.GET,
                with_resource('/' + API_VERSION + '/accounts/2iqph'),
                body=with_fixture('accounts_load'),
                content_type='application/json',
                )

        client = Client(
                characters(40),
                characters(40),
                characters(40),
                characters(40)
                )

        account = Account.load(client, '2iqph')

        # Set the client and account
        cls.client = client
        cls.account = account

    @responses.activate
    def _get_all_campaigns(self):
        # https://.../2/accounts/:account_id/campaigns
        responses.add(
                responses.GET,
                with_resource('/' + API_VERSION + '/accounts/2iqph/campaigns'),
                body=with_fixture('campaigns_all'),
                content_type='application/json',
                )

        return self.account.campaigns()

    @responses.activate
    def _get_campaign(self):
        # https://.../2/accounts/:account_id/campaigns/:campaign_id
        responses.add(
                responses.GET,
                with_resource(
                    '/' + API_VERSION + '/accounts/2iqph/campaigns/2wap7'),
                body=with_fixture('campaigns_load'),
                content_type='application/json',
                )

        return Campaign.load(self.account, '2wap7')

    def test_campaigns_all(self):
        cursor = self._get_all_campaigns()
        assert cursor is not None
        assert isinstance(cursor, Cursor)
        assert cursor.count == 10

    def test_campaign_load(self):
        campaign = self._get_campaign()
        assert campaign

    def test_campaign_entity_status_exists(self):
        campaign = self._get_campaign()
        assert campaign.entity_status
        assert campaign.entity_status == 'ACTIVE'
