#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import logging

# We have to import neovim up here and not inline.
# If we import it inline, the first few socket connections will fail
# because of timeouts.
neovim_available = None
try:
    import neovim
    neovim_available = True
except ImportError:
    neovim_available = False

class CyBldIpcNeovim():
    """
    Simple IPC integration with neovim.
    For a limited subset of commands, open the created log file
    with vims "cfile" command.

    Note that this is only available if the optional neovim python library
    is installed.
    """
    def __init__(self, enabled: bool, ipc_socket_path: str,
                 logfile_path: str, command: str):
        """
        Immediately does the IPC call if allowed.

        :param enabled: Whether the neovim integration is enabled or not
        :type enabled: bool

        :param ipc_socket_path: The path to the NVIM_LISTEN_ADDRESS socket
        :type ipc_socket_path: str

        :param logfile_path: The path to the logfile which should be opened.
        :type logfile_path: str

        :param command: The command that was executed.
        :type command: str
        """
        self._ENABLED_FOR_COMMANDS = ["make", "gcc", "g++", "tox"]

        self._enabled         = enabled
        self._ipc_socket_path = ipc_socket_path
        self._logfile_path    = logfile_path
        self._command         = command

        self._do_ipc()

    def _do_ipc(self) -> bool:
        """
        If we should do IPC, attempt to import the neovim library and open the logfile with
        vims "cfile" command.

        :rtype: bool
        :return: True if IPC was successfully done, false otherwise.
        """
        if not self._should_do_ipc:
            return False

        if not neovim_available:
            return False

        try:
            nvim = neovim.attach('socket', path=self._ipc_socket_path)
            nvim.command('cfile ' + self._logfile_path)
            nvim.command('copen')
        except:
            logging.warning("Failed to notify neovim")
            return False

        return True

    @property
    def _should_do_ipc(self) -> bool:
        """
        Check whether we should do IPC based on the enabled flag,
        the given command and the nvim IPC socket path.

        :rtype: bool
        :return: True if IPC should be done.
        """
        if not self._enabled:
            return False

        command_is_enabled = False
        for enabled_for_command in self._ENABLED_FOR_COMMANDS:
            if enabled_for_command in self._command:
                command_is_enabled = True
                break

        if command_is_enabled is False:
            return False

        if self._ipc_socket_path is None or len(self._ipc_socket_path) == 0:
            return False

        return True
