import sys, os, platform

import error
from twitter_ads.error import *
# import client
# from twitter_ads.client import *
# import resource
# from twitter_ads.resource import *
# import http
# from twitter_ads.http import *
# import account
# from twitter_ads.account import *
# import campaign_management
# from twitter_ads.campaign_management import *
# import targeting
# from twitter_ads.targeting import *
# import creative
# from twitter_ads.creative import *

VERSION = (0, 1, 0, '-rc1')

def get_version():
    if isinstance(VERSION[-1], basestring):
        return '.'.join(map(str, VERSION[:-1])) + VERSION[-1]
    return '.'.join(map(str, VERSION))

__version__ = get_version()

def enum(**enums):
    return type('Enum', (), enums)
