# Copyright (C) 2015 Twitter, Inc.

"""Container for all audience management logic used by the Ads API SDK."""

from twitter_ads.enum import TA_OPERATIONS, TRANSFORM
from twitter_ads.resource import resource_property, Resource


class TailoredAudience(Resource):

    RESOURCE_COLLECTION = '/0/accounts/{account_id}/tailored_audiences'
    RESOURCE = '/0/accounts/{account_id}/tailored_audiences/{id}'
    RESOURCE_UPDATE = '/0/accounts/{account_id}/tailored_audience_changes'
    OPT_OUT = '/0/accounts/{account_id}/tailored_audiences/global_opt_out'

    def __init__(self, account):
        self._account = account

    @property
    def account(self):
        return self._account

    @classmethod
    def create(klass, account, file_path, name, list_type):
        raise NotImplementedError

    @classmethod
    def opt_out(klass, account, file_path, list_type):
        raise NotImplementedError

    def update(self, file_path, list_type, operation=TA_OPERATIONS.ADD):
        """
        Updates the current tailored audience instance.
        """
        raise NotImplementedError

    def delete(self):
        """
        Deletes the current tailored audience instance.
        """
        raise NotImplementedError

    def status(self):
        """
        Returns the status of all changes for the current tailored
        audience instance.
        """
        raise NotImplementedError

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
