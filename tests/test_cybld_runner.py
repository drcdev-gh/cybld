#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

from unittest.mock import patch

from cybld import cybld_runner
from cybld import cybld_config_runner

# --------------------------------------------------------------------------

class TestCyBldRunner:

    def mock_system_command(self, command):
        return 0

    @patch.object(cybld_runner.CyBldRunner, '_execute_single_system_command', mock_system_command)
    def test_cybld_runner_basic(self, tmpdir_factory):
        config  = cybld_config_runner.CyBldConfigRunner("runner_python", "python", ".*test.py")
        testdir = tmpdir_factory.mktemp('runner')
        testdir.chdir()

        sut     = cybld_runner.CyBldRunner(config)

        assert(len(sut.results.previous_results) == 0)
        assert(len(sut.results.current_results)  == 0)
        assert(len(sut.params)  == 0)

        tf1 = testdir.join("mytest.py")
        tf1.write("test")

        tf2 = testdir.join("hello.py")
        tf2.write("test")

        sut._populate_params()

        assert(len(sut.results.previous_results) == 0)
        assert(len(sut.results.current_results)  == 0)
        assert(len(sut.params)  == 1)

        assert(sut.run_all() is True)

        assert(len(sut.results.previous_results) == 0)
        assert(len(sut.results.current_results)  == 1)
        assert(len(sut.params)  == 1)

        tf3 = testdir.join("mysecondtest.py")
        tf3.write("test")

        assert(sut.run_all() is True)

        assert(len(sut.results.previous_results) == 1)
        assert(len(sut.results.current_results)  == 2)
        assert(len(sut.params)  == 2)
