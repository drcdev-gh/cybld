#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import configparser
import logging
import os

from cybld import cybld_helpers

# --------------------------------------------------------------------------

class CyBldConfigKeys:
    CONFIG_SECTION_SETTINGS   = "settings"
    CONFIG_VAR_NOTIFY_SUCCESS = "notify_on_success"
    CONFIG_VAR_NOTIFY_FAIL    = "notify_on_fail"
    CONFIG_VAR_NOTIFY_TIMEOUT = "notify_timeout"
    CONFIG_VAR_BELL_SUCCESS   = "bell_on_success"
    CONFIG_VAR_BELL_FAIL      = "bell_on_fail"
    CONFIG_VAR_TMUX_SUCCESS   = "tmux_on_success"
    CONFIG_VAR_TMUX_FAIL      = "tmux_on_fail"
    CONFIG_VAR_ALLOW_MULTIPLE = "allow_multiple"
    CONFIG_VAR_PRINT_STATS    = "print_stats"
    CONFIG_VAR_TALK           = "talk"

    CONFIG_VAR_TMUX_REFRESH_STATUS = "tmux_refresh_status"

    CONFIG_VAR_CODEWORD_REGEX = "codeword_regex"
    CONFIG_VAR_ENV_REGEX      = "env_regex"
    CONFIG_VAR_CWD_REGEX      = "cwd_regex"
    CONFIG_VAR_FILE_REGEX     = "file_regex"
    CONFIG_VAR_HOSTNAME_REGEX = "hostname_regex"
    CONFIG_VAR_CMD0           = "cmd0"
    CONFIG_VAR_CMD1           = "cmd1"
    CONFIG_VAR_CMD2           = "cmd2"

    CONFIG_VAR_RUNNER_CMD          = "cmd"
    CONFIG_VAR_RUNNER_PARAM_REGEX  = "param_regex"

# --------------------------------------------------------------------------

class CyBldConfig:
    """
    CyBldConfig class, containing static key definitions and the configparser.
    In case no config could be found, this creates an initial config on startup
    """
    def __init__(self):
        self.config = configparser.ConfigParser()

        self.configfile   = None
        configfolder      = "~/"

        for possible_folder in cybld_helpers.CONFIG_FOLDERS:
            expanded_folder = os.path.expandvars(os.path.expanduser(possible_folder))
            if os.path.isdir(expanded_folder):
                configfolder = expanded_folder

                if os.path.isfile(expanded_folder + cybld_helpers.CONFIG_FILE_NAME):
                    self.configfile = expanded_folder + cybld_helpers.CONFIG_FILE_NAME
                    break

        if self.configfile:
            self.read()
        else:
            self.configfile = configfolder + cybld_helpers.CONFIG_FILE_NAME
            logging.info("creating configfile " + self.configfile)

            self.create()
            exit()

    def create(self):
        """ Creates a simple config, containing only the 'settings' section """
        self.config[CyBldConfigKeys.CONFIG_SECTION_SETTINGS] = {
            CyBldConfigKeys.CONFIG_VAR_NOTIFY_SUCCESS  : "True",
            CyBldConfigKeys.CONFIG_VAR_NOTIFY_FAIL     : "True",
            CyBldConfigKeys.CONFIG_VAR_BELL_SUCCESS    : "False",
            CyBldConfigKeys.CONFIG_VAR_BELL_FAIL       : "True",
            CyBldConfigKeys.CONFIG_VAR_TMUX_SUCCESS    : "False",
            CyBldConfigKeys.CONFIG_VAR_TMUX_FAIL       : "False",
            CyBldConfigKeys.CONFIG_VAR_ALLOW_MULTIPLE  : "False",
            CyBldConfigKeys.CONFIG_VAR_PRINT_STATS     : "True",
            CyBldConfigKeys.CONFIG_VAR_TALK            : "True",
            CyBldConfigKeys.CONFIG_VAR_NOTIFY_TIMEOUT  : "3000",
            CyBldConfigKeys.CONFIG_VAR_TMUX_REFRESH_STATUS : "False"}

        self.write()

    def write(self):
        """ Actually write the configfile """
        with open(self.configfile, 'w') as cfgfile:
            self.config.write(cfgfile)

    def read(self):
        """ Read the configfile """
        self.config.read(self.configfile)

    def add_command_group(self, command_group):
        """
        Add the new command group to the template file.

        :param command_group: The command group to write.
        :type command_group: cybld.cybld_config_command_group.CyBldConfigCommandGroup
        """
        logging.info("Adding command group " + command_group.name + " to " + self.configfile)
        self.config.add_section(command_group.name)
        section = self.config[command_group.name]
        section[CyBldConfigKeys.CONFIG_VAR_CODEWORD_REGEX] = command_group.regex_codeword.pattern
        section[CyBldConfigKeys.CONFIG_VAR_CWD_REGEX]      = command_group.regex_cwd.pattern
        section[CyBldConfigKeys.CONFIG_VAR_ENV_REGEX]      = command_group.regex_env.pattern
        section[CyBldConfigKeys.CONFIG_VAR_FILE_REGEX]     = command_group.regex_file.pattern
        section[CyBldConfigKeys.CONFIG_VAR_HOSTNAME_REGEX] = command_group.regex_hostname.pattern
        section[CyBldConfigKeys.CONFIG_VAR_CMD0]           = command_group.cmd0
        section[CyBldConfigKeys.CONFIG_VAR_CMD1]           = command_group.cmd1
        section[CyBldConfigKeys.CONFIG_VAR_CMD2]           = command_group.cmd2

        self.write()

    def _sanity_check_config_section_variable(variable):
        def decorator(func):
            def func_wrapper(self, section):
                if section not in self.config.sections():
                    logging.fatal("CONFIG ERROR: Config section " + section +
                                  " does not exist")
                    exit(1)

                if variable not in self.config[section]:
                    logging.fatal("CONFIG ERROR: Variable " + variable +
                                  " does not exist in section " + section)
                    exit(1)

                return func(self, section)
            return func_wrapper
        return decorator

    def get_notify_success(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_NOTIFY_SUCCESS)

    def get_notify_fail(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_NOTIFY_FAIL)

    def get_notify_timeout(self):
        return self.config.getint(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                  CyBldConfigKeys.CONFIG_VAR_NOTIFY_TIMEOUT)

    def get_bell_success(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_BELL_SUCCESS)

    def get_bell_fail(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_BELL_FAIL)

    def get_tmux_success(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_TMUX_SUCCESS)

    def get_tmux_fail(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_TMUX_FAIL)

    def get_tmux_refresh_status(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_TMUX_REFRESH_STATUS)

    def get_allow_multiple(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_ALLOW_MULTIPLE)

    def get_print_stats(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_PRINT_STATS)

    def get_talk(self):
        return self.config.getboolean(CyBldConfigKeys.CONFIG_SECTION_SETTINGS,
                                      CyBldConfigKeys.CONFIG_VAR_TALK)

    def get_command_groups(self):
        sections = self.config.sections()
        sections.remove(CyBldConfigKeys.CONFIG_SECTION_SETTINGS)

        for section in sections[:]:
            if section.startswith(cybld_helpers.CONFIG_RUNNER_INDICATOR):
                sections.remove(section)

        return sections

    def get_runners(self):
        sections = self.config.sections()
        sections.remove(CyBldConfigKeys.CONFIG_SECTION_SETTINGS)

        for section in sections[:]:
            if not section.startswith(cybld_helpers.CONFIG_RUNNER_INDICATOR):
                sections.remove(section)

        return sections

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_RUNNER_CMD)
    def get_runner_command(self, runner_section):
        return self.config[runner_section][CyBldConfigKeys.CONFIG_VAR_RUNNER_CMD]

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_RUNNER_PARAM_REGEX)
    def get_runner_regex_find_params(self, runner_section):
        return self.config[runner_section][CyBldConfigKeys.CONFIG_VAR_RUNNER_PARAM_REGEX]

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_CODEWORD_REGEX)
    def get_command_group_codeword_regex(self, section):
        return self.config[section][CyBldConfigKeys.CONFIG_VAR_CODEWORD_REGEX]

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_ENV_REGEX)
    def get_command_group_env_regex(self, section):
        return self.config[section][CyBldConfigKeys.CONFIG_VAR_ENV_REGEX]

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_CWD_REGEX)
    def get_command_group_cwd_regex(self, section):
        return self.config[section][CyBldConfigKeys.CONFIG_VAR_CWD_REGEX]

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_HOSTNAME_REGEX)
    def get_command_group_hostname_regex(self, section):
        return self.config[section][CyBldConfigKeys.CONFIG_VAR_HOSTNAME_REGEX]

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_FILE_REGEX)
    def get_command_group_file_regex(self, section):
        return self.config[section][CyBldConfigKeys.CONFIG_VAR_FILE_REGEX]

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_CMD0)
    def get_command_group_cmd0(self, section):
        return self.config[section][CyBldConfigKeys.CONFIG_VAR_CMD0]

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_CMD1)
    def get_command_group_cmd1(self, section):
        return self.config[section][CyBldConfigKeys.CONFIG_VAR_CMD1]

    @_sanity_check_config_section_variable(CyBldConfigKeys.CONFIG_VAR_CMD2)
    def get_command_group_cmd2(self, section):
        return self.config[section][CyBldConfigKeys.CONFIG_VAR_CMD2]
