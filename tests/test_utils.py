import datetime
from random import randint

from twitter_ads.enum import GRANULARITY
from twitter_ads.utils import size, to_time


t = datetime.datetime(2006, 3, 21, 0, 0, 0)

def test_to_time_based_on_granularity():
    for g in [None, GRANULARITY.HOUR, GRANULARITY.TOTAL]:
        assert to_time(t, g) == '2006-03-21T00:00:00Z'
    assert to_time(t, GRANULARITY.DAY) == '2006-03-21'

def test_sizes():
    _DEFAULT_CHUNK_SIZE = 64
    _RESPONSE_TIME_MAX = 5000
    for _ in range(10):
        response_time = randint(0, _RESPONSE_TIME_MAX)
        assert size(_DEFAULT_CHUNK_SIZE, _RESPONSE_TIME_MAX, response_time) == _DEFAULT_CHUNK_SIZE
    response_times = {10000 : 32,
                      20000 : 16,
                      40000 : 8,
                      80000 : 4,
                      160000 : 2,
                      320000 : 1}
    for rt in response_times:
        assert size(_DEFAULT_CHUNK_SIZE, _RESPONSE_TIME_MAX, rt) == response_times[rt]
