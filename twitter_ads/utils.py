# Copyright (C) 2015 Twitter, Inc.

"""Container for all helpers and utilities used throughout the Ads API SDK."""

import datetime

from twitter_ads import VERSION
from twitter_ads.enum import GRANULARITY


def get_version():
    if isinstance(VERSION[-1], str):
        return '.'.join(map(str, VERSION[:-1])) + VERSION[-1]
    return '.'.join(map(str, VERSION))


def to_time(time, granularity):
    if not granularity:
        return format_time(time)
    if granularity == GRANULARITY.HOUR:
        return format_time(time - datetime.timedelta(
            minutes=time.minute, seconds=time.second, microseconds=time.microsecond))
    elif granularity == GRANULARITY.DAY:
        return format_time(time - datetime.timedelta(
            hours=time.hour, minutes=time.minute,
            seconds=time.second, microseconds=time.microsecond))
    else:
        return format_time(time)


def format_time(time):
    return time.strftime('%Y-%m-%dT%H:%M:%SZ')
