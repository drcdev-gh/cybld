#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

from cybld import cybld_command_stats
from cybld import cybld_helpers

# --------------------------------------------------------------------------

class TestCyBldCommandStats:

    def test_command_stats(self):
        sut  = cybld_command_stats.CyBldCommandStats("mycmd")

        sut.update_stats(True, 5)
        assert(sut._get_avg_runtime() == 5)
        assert(cybld_helpers.ICON_SUCCESS in sut.get_stats_str())
        assert(cybld_helpers.ICON_FAIL not in sut.get_stats_str())
        assert(cybld_helpers.ICON_UNKNOWN in sut.get_stats_str())

        sut.update_stats(False, 15)
        assert(sut._get_avg_runtime() == 10)
        assert(cybld_helpers.ICON_SUCCESS in sut.get_stats_str())
        assert(cybld_helpers.ICON_FAIL in sut.get_stats_str())
        assert(cybld_helpers.ICON_UNKNOWN in sut.get_stats_str())

        sut.update_stats(False, 30)
        assert(sut._get_avg_runtime() == 16)
        assert(cybld_helpers.ICON_SUCCESS in sut.get_stats_str())
        assert(cybld_helpers.ICON_FAIL in sut.get_stats_str())
        assert(cybld_helpers.ICON_UNKNOWN in sut.get_stats_str())

        sut.update_stats(False, 30)
        assert(sut._get_avg_runtime() == 20)
        assert(cybld_helpers.ICON_SUCCESS in sut.get_stats_str())
        assert(cybld_helpers.ICON_FAIL in sut.get_stats_str())
        assert(cybld_helpers.ICON_UNKNOWN in sut.get_stats_str())

        sut.update_stats(False, 20)
        assert(sut._get_avg_runtime() == 20)
        assert(cybld_helpers.ICON_SUCCESS in sut.get_stats_str())
        assert(cybld_helpers.ICON_FAIL in sut.get_stats_str())
        assert(cybld_helpers.ICON_UNKNOWN not in sut.get_stats_str())

        sut.update_stats(False, 5)
        assert(sut._get_avg_runtime() == 20)
        assert(cybld_helpers.ICON_SUCCESS not in sut.get_stats_str())
        assert(cybld_helpers.ICON_FAIL in sut.get_stats_str())
        assert(cybld_helpers.ICON_UNKNOWN not in sut.get_stats_str())
