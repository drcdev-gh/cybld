#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import os
import re

from cybld import cybld_helpers

# --------------------------------------------------------------------------

class CyBldConfigCommandGroup:
    """
    Representation of a configured command group. Provides a few simple
    functions to check if regex conditions are fulfilled.

    :param name:           The name of the command group (config section key).
    :type name:            str

    :param regex_codeword: The codeword regular expression which has to match.
    :type regex_codeword:  str

    :param regex_env:      The env regular expression which has to match
                           (env variable CYPROJECT).
    :type regex_env:       str

    :param regex_cwd:      The current working dir regular expression which has
                           to match.
    :type regex_cwd:       str

    :param regex_hostname: The hostname regular expression which has to match.
    :type regex_hostname:  str

    :param regex_file:     The file regular expression which has to match (all
                           files in current dir).
    :type regex_file:      str

    :param cmd0:           cmd0 as string.
    :type cmd0:            str

    :param cmd1:           cmd1 as string.
    :type cmd1:            str

    :param cmd2:           cmd2 as string.
    :type cmd2:            str
    """
    def __init__(self, name, regex_codeword, regex_env, regex_cwd, regex_hostname,
                 regex_file, cmd0, cmd1, cmd2):
        self.name           = name
        self.regex_codeword = re.compile(regex_codeword)
        self.regex_env      = re.compile(regex_env)
        self.regex_cwd      = re.compile(regex_cwd)
        self.regex_hostname = re.compile(regex_hostname)
        self.regex_file     = re.compile(regex_file)
        self.cmd0           = cmd0
        self.cmd1           = cmd1
        self.cmd2           = cmd2

    def codeword_regex_matches(self, codeword = None):
        """
        :type codeword: str
        """
        if codeword is None:
            return True

        return self.regex_codeword.match(codeword)

    def is_cmd0_runner(self):
        return self.is_cmd_runner_command(self.cmd0)

    def is_cmd1_runner(self):
        return self.is_cmd_runner_command(self.cmd1)

    def is_cmd2_runner(self):
        return self.is_cmd_runner_command(self.cmd2)

    def is_cmd_runner_command(self, cmd):
        return cmd.startswith(cybld_helpers.CONFIG_RUNNER_INDICATOR)

    def env_regex_matches(self):
        env_value = os.getenv(cybld_helpers.ENV_KEY, "DEFAULT")
        return self.regex_env.match(env_value)

    def cwd_regex_matches(self):
        return self.regex_cwd.match(os.getcwd())

    def hostname_regex_matches(self):
        hostname_env_value = os.getenv("HOSTNAME")
        return self.regex_hostname.match(str(hostname_env_value))

    def file_regex_matches(self):
        for filename in os.listdir(os.curdir):
            if self.regex_file.match(filename):
                return True

        return False
