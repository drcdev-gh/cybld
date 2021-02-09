#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import atexit
import sys

import logging
import os
import pickle
import socket
import string
from cybld import cybld_helpers
from cybld.cybld_command_handler import CyBldCommandHandler
from cybld.cybld_config_command_group import CyBldConfigCommandGroup
from cybld.cybld_config_settings import CyBldConfigSettings
from cybld.cybld_notifier import CyBldNotifier

# --------------------------------------------------------------------------

class CyBldIpcServer():
    """
    Provides the IPC service.

    Initializes the IPC socket and starts the main loop.
    Uses CyBldCommandHandler and CyBldNotifier internally.

    :param command_group:     command group (cmd0, cmd1, cmd2) with which
                              this instance has been started with (read from
                              config)
    :type command_group:      cybld_config.CyBldConfigCommandGroup

    :param do_notify_success: whether to use "notify-send" when a given command
                              was executed successfully (read from config)
    :type do_notify_success:  bool

    :param do_notify_fail:    whether to use "notify-send" when a given command
                              was executed unsuccessfully (read from config)
    :type do_notify_fail:     bool

    :param timeout:           the timeout for notifications
    :type timeout:            int

    :param do_bell_success:   whether to ring the bell when a given command
                              was executed successfully (read from config)
    :type do_bell_success:    bool

    :param do_bell_fail:      whether to ring the bell when a given command
                              was executed unsuccessfully (read from config)
    :type do_bell_fail:       bool

    :param allow_multiple_instances: we quit if this is false and there is
                                     already an instance running
    :type allow_multiple_instances:  bool

    :param print_stats:       whether to print command statistics
    :type print_stats:        bool

    :param talk:              whether we should print conversational messages or
                              not
    :type talk:               bool
    """

    def __init__(self, command_group: CyBldConfigCommandGroup, runner_configs,
                 settings: CyBldConfigSettings):

        # This handler should be executed at the end, since it also removes
        # the base directory in case no cybld session is left
        atexit.register(self._close_socket)

        self.settings        = settings
        self.notifier        = CyBldNotifier(settings)
        self.command_handler = CyBldCommandHandler(command_group, runner_configs, settings,
                                                   self.notifier.notify_success,
                                                   self.notifier.notify_fail)

        self.server          = None
        self.socket_name     = self._generate_new_random_socket_name()

        if not settings.allow_multiple:
            self._quit_if_instance_exists()

        logging.info("Starting with " + cybld_helpers.BOLD_TEXT +
                     command_group.name + cybld_helpers.COLOR_END +
                     " config (" + self.socket_name + ")")
        logging.info("The codeword has to match " + cybld_helpers.BOLD_TEXT +
                     command_group.regex_codeword.pattern + cybld_helpers.COLOR_END)
        logging.info("Commands are: " +
                     "\n" + "- CMD0: " + command_group.cmd0 +
                     "\n" + "- CMD1: " + command_group.cmd1 +
                     "\n" + "- CMD2: " + command_group.cmd2)
        cybld_helpers.print_seperator_lines()

        self._open_socket()
        self._start_main_loop()

    def _generate_new_random_socket_name(self):
        """ Use the next available cybld socket name (letters a-z) """
        current_socket_names = cybld_helpers.get_current_socket_names()
        for letter in string.ascii_lowercase:
            socket_name = cybld_helpers.SOCKET_BASE_NAME + "-" + letter
            if socket_name not in current_socket_names:
                return socket_name
        logging.critical("Too many instances already running...")
        sys.exit(1)

    def _quit_if_instance_exists(self):
        """ Exit if a cybld instance is already running """
        current_socket_names = cybld_helpers.get_current_socket_names()
        if len(current_socket_names) > 0:
            logging.critical("IPC socket is already started!")
            sys.exit(1)

    def _open_socket(self):
        """ Open a new socket (with the previously generated socket name) """
        assert(self.server is None)

        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
        self.server.bind(os.path.join(cybld_helpers.get_base_path(), self.socket_name))

    def _start_main_loop(self):
        """
        Start the main loop.

        Wait for incoming messages on the socket, "parse" them via pickle and
        then forward the command to the command handler.
        """
        assert(self.server is not None)

        try:
            while True:
                data = self.server.recv(1024)
                if not data:
                    break
                else:
                    cmd = pickle.loads(data)
                    self.command_handler.handle_incoming_ipc_message(cmd)
        except:
            pass

    def _close_socket(self):
        """ Close the IPC socket (at shutdown) """
        logging.info("Shutdown initiated for " + self.socket_name)
        self.server.close()
        os.remove(os.path.join(cybld_helpers.get_base_path(), self.socket_name))

        files_in_base_path = os.listdir(cybld_helpers.get_base_path())
        for f in files_in_base_path:
            if f.startswith(cybld_helpers.NVIM_LOG_PREFIX):
                os.remove(os.path.join(cybld_helpers.get_base_path(), f))

        if len(cybld_helpers.get_current_socket_names()) == 0:
            logging.info("This was the last cybld session!")
            os.rmdir(cybld_helpers.get_base_path())

# --------------------------------------------------------------------------
