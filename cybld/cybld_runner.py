#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import os
import time

from cybld.cybld_config_runner import CyBldConfigRunner
from cybld.cybld_runner_results import CyBldRunnerResults, CyBldRunnerSingleResult, CyBldRunnerResultType


class CyBldRunner:
    """
    Provides the possibility to run a command multiple times with found files as parameter.

    :param config:     the configuration of the runner
    :type config:      cybld_config_runner.CyBldConfigRunner
    """

    def __init__(self, config: CyBldConfigRunner):
        self.config  = config
        self.results = CyBldRunnerResults()
        self.params  = []

        self._populate_params()

    def run_all(self):
        """
        "Moves" the current result set to the previous result set and then executes each command/param
        after another via _run_single.

        Also prints the results in a pretty way.

        :return:    Returns True if every command succeeded, False otherwise.
        """
        self.results.finish()
        self._populate_params()

        success = True
        for param in self.params:
            if not self._run_single(param):
                success = False

        self._to_string()
        return success

    def _to_string(self):
        """ Simple helper method printing both the results and te comparion """
        self.results.print_results()
        self.results.print_comparison()

    def _populate_params(self):
        """ Recursively find all files matching the configured regex and add them to self.params """
        self.params = []
        for root, dirs, files in os.walk(os.curdir):
            for file in files:
                fullfile = str(os.path.join(root, file))
                if self.config.regex_find_params.match(fullfile):
                    self.params.append(fullfile)

    def _run_single(self, param: str):
        """ Run the command (while timing it) and store the result """
        single_result = CyBldRunnerSingleResult(self.config.command, param)

        start = time.time()

        success = False
        if self._execute_single_system_command(self.config.command + " " + param) == 0:
            success = True

        end = time.time()

        if success:
            single_result.set_result(CyBldRunnerResultType.success,
                                     int(end - start))
        else:
            single_result.set_result(CyBldRunnerResultType.fail,
                                     int(end - start))

        self.results.add_result(single_result)
        return success

    def _execute_single_system_command(self, command: str):
        return os.system(command)
