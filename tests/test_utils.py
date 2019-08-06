import datetime

from twitter_ads.enum import GRANULARITY
from twitter_ads.utils import to_time, Deprecated


t = datetime.datetime(2006, 3, 21, 0, 0, 0)


def test_to_time_based_on_granularity():
    for g in [None, GRANULARITY.HOUR, GRANULARITY.TOTAL]:
        assert to_time(t, g) == '2006-03-21T00:00:00Z'
    assert to_time(t, GRANULARITY.DAY) == '2006-03-21'


def test_decorator_deprecated():
    import warnings

    class TestClass(object):
        @classmethod
        @Deprecated('deprecated API')
        def test(self):
            pass

    with warnings.catch_warnings(record=True) as log:
        TestClass.test()
        assert len(log) == 1
        assert issubclass(log[-1].category, DeprecationWarning)
        assert "TestClass.test" in str(log[-1].message)
        assert "deprecated API" in str(log[-1].message)
