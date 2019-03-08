# Copyright (C) 2015 Twitter, Inc.
from __future__ import division

"""Container for all helpers and utilities used throughout the Ads API SDK."""

import datetime
from datetime import timedelta
import dateutil.parser
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


def size(default_chunk_size, response_time_max, response_time_actual):
    """Determines the chunk size based on response times."""
    if response_time_actual == 0:
        response_time_actual = 1
    scale = 1 / (response_time_actual / response_time_max)
    size = int(default_chunk_size * scale)
    return min(max(size, 1), default_chunk_size)


def date_range(data, fetch_frequency):
    """Returns the minimum activity start time and the maximum activity end time
    from the active entities response. These are the dates that should be used
    in the subsequent analytics request. The max time is modified
    """
    start = min([dateutil.parser.parse(d['activity_start_time']) for d in data])
    end = max([dateutil.parser.parse(d['activity_end_time']) for d in data])
    if fetch_frequency == 'HOUR':
        start = remove_minutes(start)
        end = remove_minutes(end) + timedelta(hours=1)
    elif fetch_frequency == 'DAY':
        start = remove_hours(start)
        end = remove_hours(end) + timedelta(days=1)
    else:
        raise ValueError("Only 'HOUR' or 'DAY' values are accepted.")
    return start, end
