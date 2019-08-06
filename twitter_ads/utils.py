# Copyright (C) 2015 Twitter, Inc.
from __future__ import division

"""Container for all helpers and utilities used throughout the Ads API SDK."""

import datetime
import warnings
warnings.simplefilter('default', DeprecationWarning)
from email.utils import formatdate
from time import mktime

from twitter_ads import VERSION
from twitter_ads.enum import GRANULARITY


def get_version():
    """Returns a string representation of the current SDK version."""
    if isinstance(VERSION[-1], str):
        return '.'.join(map(str, VERSION[:-1])) + VERSION[-1]
    return '.'.join(map(str, VERSION))


def remove_minutes(time):
    """Sets the minutes, seconds, and microseconds to zero."""
    return time.replace(minute=0, second=0, microsecond=0)


def remove_hours(time):
    """Sets the hours, minutes, seconds, and microseconds to zero."""
    return time.replace(hour=0, minute=0, second=0, microsecond=0)


def to_time(time, granularity):
    """Returns a truncated and rounded time string based on the specified granularity."""
    if not granularity:
        if type(time) is datetime.date:
            return format_date(time)
        else:
            return format_time(time)
    if granularity == GRANULARITY.HOUR:
        return format_time(remove_minutes(time))
    elif granularity == GRANULARITY.DAY:
        return format_date(remove_hours(time))
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


def validate_whole_hours(time):
    if type(time) is datetime.date:
        pass
    else:
        # Times must be expressed in whole hours
        if time.minute > 0 or time.second > 0:
            raise ValueError("'start_time' and 'end_time' must be expressed in whole hours.")


def extract_response_headers(headers):
    values = {}

    values['rate_limit'] = headers.get('x-rate-limit-limit')
    values['rate_limit_remaining'] = headers.get('x-rate-limit-remaining')
    values['rate_limit_reset'] = headers.get('x-rate-limit-reset')

    values['account_rate_limit'] = headers.get('x-account-rate-limit-limit')
    values['account_rate_limit_remaining'] = headers.get('x-account-rate-limit-remaining')
    values['account_rate_limit_reset'] = headers.get('x-account-rate-limit-reset')

    return values


class Deprecated(object):
    def __init__(self, message):
        self._message = message

    def __call__(self, decorated, *args, **kwargs):
        def wrapper(*args, **kwargs):
            method = str(decorated.__qualname__)
            warnings.warn(
                "{} => {}".format(method, self._message),
                DeprecationWarning,
                stacklevel=2
            )
            return decorated(*args, **kwargs)
        return wrapper
