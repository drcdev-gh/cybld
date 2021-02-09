#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import cybld.cybld_config_command_group

# --------------------------------------------------------------------------

template_cpp    = cybld.cybld_config_command_group.CyBldConfigCommandGroup(
        "cpp", ".*.h|.*.cpp|.*.cmake",
        ".*", ".*", ".*", "CMakeCache.txt",
        "make", "make test", "make clean")
template_python = cybld.cybld_config_command_group.CyBldConfigCommandGroup(
        "python", ".*.py|.*.ini",
        ".*", ".*", ".*", "tox.ini",
        "tox", "py.test", "python setup.py develop")

# --------------------------------------------------------------------------

templates = {"cpp": template_cpp,
             "python": template_python}
