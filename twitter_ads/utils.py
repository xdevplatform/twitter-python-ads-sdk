# Copyright (C) 2015 Twitter, Inc.

"""Container for all helpers and utilities used throughout the Ads API SDK."""

from twitter_ads import VERSION


def get_version():
    if isinstance(VERSION[-1], str):
        return '.'.join(map(str, VERSION[:-1])) + VERSION[-1]
    return '.'.join(map(str, VERSION))
