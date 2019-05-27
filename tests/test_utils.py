import datetime
from random import randint

from twitter_ads.enum import GRANULARITY
from twitter_ads.utils import to_time


t = datetime.datetime(2006, 3, 21, 0, 0, 0)

def test_to_time_based_on_granularity():
    for g in [None, GRANULARITY.HOUR, GRANULARITY.TOTAL]:
        assert to_time(t, g) == '2006-03-21T00:00:00Z'
    assert to_time(t, GRANULARITY.DAY) == '2006-03-21'
