#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

from cybld import cybld_helpers

# --------------------------------------------------------------------------


class CyBldCommandStatsList:
    """
    A simple list of CyBldCommandStats. Only once instance of this should exist
    """

    def __init__(self):
        self._command_stats = []

    def update_command_stats(self, command: str, success_or_fail: bool, run_time: int):
        """
        Update the statistics of the given command.

        :param command:         The command (as string)
        :param success_or_fail: Whether the command was successful or not (ret 0
                                means success)
        :param run_time:        How long the command took (in seconds)
        """
        target_command = None
        for stored_command in self._command_stats:
            if stored_command.command == command:
                target_command = stored_command

        if target_command is None:
            target_command = CyBldCommandStats(command)
            self._command_stats.append(target_command)

        target_command.update_stats(success_or_fail, run_time)

    def get_command_stats(self, command: str) -> str:
        """
        Getter for a given specific command.

        :param command: The command as string
        """
        for stored_command in self._command_stats:
            if stored_command.command == command:
                return stored_command.get_stats_str()

        return 'No previous runs recorded'

# --------------------------------------------------------------------------


class CyBldCommandStats:
    """
    A simple data object, which keeps track of the 5 most recent runs of a
    command.

    :param command: The command as string
    """

    def __init__(self, command: str):
        self._command    = command
        self._exit_codes = []
        self._run_times  = []

    @property
    def command(self) -> str:
        return self._command

    def update_stats(self, success_or_fail: bool, run_time: int):
        """
        Update the statistics by appending the exit code and the run time.
        In case we already have stored > 5 runs, the first run is removed.

        :param success_or_fail: Whether the command was successful or not
        :param run_time:        How long the command took (in seconds)
        """
        # Store max of 5 runs
        if len(self._exit_codes) >= 5:
            self._exit_codes.pop(0)
        if len(self._run_times) >= 5:
            self._run_times.pop(0)

        self._exit_codes.append(success_or_fail)
        self._run_times.append(int(run_time))

    def get_stats_str(self):
        """ Returns a printable representation of the stats """
        ret            = 'previous runs: '
        ret_exit_codes = ""

        for exit_code in self._exit_codes:
            if exit_code:
                ret_exit_codes = ret_exit_codes + cybld_helpers.ICON_SUCCESS
            else:
                ret_exit_codes = ret_exit_codes + cybld_helpers.ICON_FAIL

            ret_exit_codes += " "

        while len(ret_exit_codes) < 10:
            ret_exit_codes = ret_exit_codes + cybld_helpers.ICON_UNKNOWN + " "

        ret = "{0}{1} ".format(ret, ret_exit_codes)
        ret = "{0}(avg. {1} seconds)".format(ret, str(self._get_avg_runtime()))
        return ret

    def _get_avg_runtime(self):
        """ Calculate a simple arithmetic average of the run time """
        run_time_total = 0
        for run_time in self._run_times:
            run_time_total = run_time_total + run_time

        return int(run_time_total / len(self._run_times))
