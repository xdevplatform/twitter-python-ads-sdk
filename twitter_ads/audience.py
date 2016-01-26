# Copyright (C) 2015 Twitter, Inc.

"""Container for all audience management logic used by the Ads API SDK."""

from twitter_ads.enum import TA_OPERATIONS, TRANSFORM
from twitter_ads.resource import resource_property, Resource
from twitter_ads.http import TONUpload, Request
from twitter_ads.error import BadRequest
from twitter_ads.cursor import Cursor


class TailoredAudience(Resource):

    PROPERTIES = {}

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/tailored_audiences'
    RESOURCE = '/0/accounts/{account_id}/tailored_audiences/{id}'
    RESOURCE_UPDATE = '/0/accounts/{account_id}/tailored_audience_changes'
    OPT_OUT = '/0/accounts/{account_id}/tailored_audiences/global_opt_out'

    @classmethod
    def create(klass, account, file_path, name, list_type):
        """
        Uploads and creates a new tailored audience.
        """
        upload = TONUpload(account.client, file_path)
        audience = klass(account)
        getattr(audience, '__create_audience__')(name, list_type)
        try:
            getattr(audience, '__update_audience__')(upload.perform(), list_type, TA_OPERATIONS.ADD)
            return audience.reload()
        except BadRequest as e:
            audience.delete()
            raise e

    @classmethod
    def opt_out(klass, account, file_path, list_type):
        """
        Updates the global opt-out list for the specified advertiser account.
        """
        upload = TONUpload(account.client, file_path)
        params = {'input_file_path': upload.perform(), 'list_type': list_type}
        resource = klass.OPT_OUT.format(account_id=account.id)
        Request(account.client, 'put', resource, params=params).perform()
        return True

    def update(self, file_path, list_type, operation=TA_OPERATIONS.ADD):
        """
        Updates the current tailored audience instance.
        """
        upload = TONUpload(self.account.client, file_path)
        getattr(self, '__update_audience__')(upload.perform(), list_type, operation)
        return self.reload()

    def delete(self):
        """
        Deletes the current tailored audience instance.
        """
        resource = self.RESOURCE.format(account_id=self.account.id, id=self.id)
        response = Request(self.account.client, 'delete', resource).perform()
        return self.from_response(response.body['data'])

    def status(self):
        """
        Returns the status of all changes for the current tailored audience instance.
        """
        if not self.id:
            return None

        resource = self.RESOURCE_UPDATE.format(account_id=self.account.id)
        request = Request(self.account.client, 'get', resource, params=self.to_params())
        cursor = list(Cursor(None, request))

        return filter(lambda change: change['tailored_audience_id'] == self.id, cursor)

    def __create_audience__(self, name, list_type):
        params = {'name': name, 'list_type': list_type}
        resource = self.RESOURCE_COLLECTION.format(account_id=self.account.id)
        response = Request(self.account.client, 'post', resource, params=params).perform()
        return self.from_response(response.body['data'])

    def __update_audience__(self, location, list_type, operation):
        params = {
            'tailored_audience_id': self.id,
            'input_file_path': location,
            'list_type': list_type,
            'operation': operation
        }

        resource = self.RESOURCE_UPDATE.format(account_id=self.account.id)
        return Request(self.account.client, 'post', resource, params=params).perform()

# tailored audience properties
# read-only
resource_property(TailoredAudience, 'id', readonly=True)
resource_property(TailoredAudience, 'created_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(TailoredAudience, 'updated_at', readonly=True, transform=TRANSFORM.TIME)
resource_property(TailoredAudience, 'deleted', readonly=True, transform=TRANSFORM.BOOL)
resource_property(TailoredAudience, 'audience_size', readonly=True)
resource_property(TailoredAudience, 'audience_type', readonly=True)
resource_property(TailoredAudience, 'metadata', readonly=True)
resource_property(TailoredAudience, 'partner_source', readonly=True)
resource_property(TailoredAudience, 'reasons_not_targetable', readonly=True)
resource_property(TailoredAudience, 'targetable', readonly=True)
resource_property(TailoredAudience, 'targetable_types', readonly=True)
# writable
resource_property(TailoredAudience, 'name')
resource_property(TailoredAudience, 'list_type')
