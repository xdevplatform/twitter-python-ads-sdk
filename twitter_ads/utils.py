# Copyright (C) 2015 Twitter, Inc.
from __future__ import division

"""Container for all helpers and utilities used throughout the Ads API SDK."""

import datetime
import re
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
    # only get "X-${name}" custom response headers
    reg = re.compile(r"^x-", re.IGNORECASE)
    for i in headers:
        if reg.match(i):
            values[i.lstrip('x-').replace('-', '_')] = headers[i]

    return values


def split_list(list_, n):
    """Splits a list by a given number (n) and returns a generator object."""
    list_size = len(list_)
    for sp in range(0, list_size, n):
        yield list_[sp:min(sp + n, list_size)]


class Deprecated(object):
    def __init__(self, message):
        self._message = message

    def __call__(self, decorated, *args, **kwargs):
        def wrapper(*args, **kwargs):
            method = "{}.{}".format(str(args[0].__name__), str(decorated.__name__))
            warnings.warn(
                "{} => {}".format(method, self._message),
                DeprecationWarning,
                stacklevel=2
            )
            return decorated(*args, **kwargs)
        return wrapper


class FlattenParams(object):
    def __init__(self, function):
        self._func = function

    def __call__(self, *args, **kwargs):
        params = kwargs
        for i in params:
            if isinstance(params[i], list):
                params[i] = ','.join(map(str, params[i]))
            elif isinstance(params[i], bool):
                params[i] = str(params[i]).lower()
        return self._func(*args, **params)
