# Copyright (C) 2015 Twitter, Inc.
from __future__ import division

"""Container for all helpers and utilities used throughout the Ads API SDK."""

from datetime import timedelta
from email.utils import formatdate
from time import mktime

from twitter_ads import VERSION
from twitter_ads.enum import GRANULARITY


def get_version():
    """Returns a string representation of the current SDK version."""
    if isinstance(VERSION[-1], str):
        return '.'.join(map(str, VERSION[:-1])) + VERSION[-1]
    return '.'.join(map(str, VERSION))


def to_time(time, granularity):
    """Returns a truncated and rounded time string based on the specified granularity."""
    if not granularity:
        return format_time(time)
    if granularity == GRANULARITY.HOUR:
        return format_time(time - timedelta(
            minutes=time.minute, seconds=time.second, microseconds=time.microsecond))
    elif granularity == GRANULARITY.DAY:
        return format_date(time - timedelta(
            hours=time.hour, minutes=time.minute,
            seconds=time.second, microseconds=time.microsecond))
    else:
        return format_time(time)


def format_time(time):
    """Formats a datetime as an ISO 8601 compliant string."""
    return time.strftime('%Y-%m-%dT%H:%M:%SZ')


def format_date(time):
    """Formats a datetime as an ISO 8601 compliant string, dropping time."""
    return time.strftime('%Y-%m-%d')


def http_time(time):
    """Formats a datetime as an RFC 1123 compliant string."""
    return formatdate(timeval=mktime(time.timetuple()), localtime=False, usegmt=True)

def size(default_chunk_size, response_time_max, response_time_actual):
    if response_time_actual == 0:
        response_time_actual = 1
    scale = 1 / (response_time_actual / response_time_max)
    size = int(default_chunk_size * scale)
    return min(max(size, 1), default_chunk_size)
