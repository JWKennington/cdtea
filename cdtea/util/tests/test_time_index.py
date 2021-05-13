"""Tests for EquivDict utility"""
import collections

from cdtea.util import TimeIndex


class TestTimeIndex:
    """Tests for TimeIndex manipulation"""
    def test_time_sep(self):
        assert TimeIndex.time_sep(2, 8, 10) == -4
        assert TimeIndex.time_sep(8, 2, 10) == 4
        assert TimeIndex.time_sep(8, 8, 10) == 0
