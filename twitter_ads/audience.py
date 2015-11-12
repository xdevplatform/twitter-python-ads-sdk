# Copyright (C) 2015 Twitter, Inc.

"""Container for all audience management logic used by the Ads API SDK."""

from twitter_ads.enum import TA_OPERATIONS
from twitter_ads.resource import resource, Resource


@resource
class TailoredAudience(Resource):

    PROPERTIES = {
        'id': {'readonly': True},
        'created_at': {'readonly': True, 'transform': 'time'},
        'updated_at': {'readonly': True, 'transform': 'time'},
        'deleted': {'readonly': True},
        'audience_size': {'readonly': True},
        'audience_type': {'readonly': True},
        'metadata': {'readonly': True},
        'partner_source': {'readonly': True},
        'reasons_not_targetable': {'readonly': True},
        'targetable': {'readonly': True},
        'targetable_types': {'readonly': True},
        'name': {},
        'list_type': {}
    }

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
