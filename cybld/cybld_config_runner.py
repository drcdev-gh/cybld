#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import re

from cybld import cybld_helpers

# --------------------------------------------------------------------------

class CyBldConfigRunner:
    def __init__(self, name: str, command: str, regex_find_params):
        self.name              = name
        self.command           = command
        self.regex_find_params = re.compile(regex_find_params)

        assert(self.name.startswith(cybld_helpers.CONFIG_RUNNER_INDICATOR))
