#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import sys
import os
import shutil
import logging
from sys import platform as _platform_

from cybld.cybld_config_settings import CyBldConfigSettings
from cybld import cybld_tmux_wrapper

# --------------------------------------------------------------------------

class CyBldNotifier:
    """ Helper class to handle notification sending """

    def __init__(self, settings: CyBldConfigSettings):

        self.settings = settings

        self._check_notify()

    def notify_success(self, msg):
        """ If so configured, send success message via notify-send and/or ring bell """
        if self.settings.bell_success:
            self._ring_bell()

        if self.settings.notify_success is True:
            self._notify_system_success(msg)

        if self.settings.tmux_success is True:
            self._notify_tmux_success(msg)

    def notify_fail(self, msg):
        """ If so configured, send fail message via notify-send and/or ring bell """
        if self.settings.bell_fail:
            self._ring_bell()

        if self.settings.notify_fail is True:
            self._notify_system_fail(msg)

        if self.settings.tmux_fail is True:
            self._notify_tmux_fail(msg)

    def _ring_bell(self):
        print("\a")

    def _notify_system_success(self, msg):
        if _platform_ == "linux":
            notify_cmd = "notify-send -a cybld -t " + str(self.settings.notify_timeout) + \
                         " 'cybld - success' " + "'" + msg + "'"
        elif _platform_ == "darwin":
            notify_cmd = "osascript -e 'display notification \"" + msg + "\"" + \
                         " with title \"cybld - success\"'"

        os.system(notify_cmd)

    def _notify_system_fail(self, msg):
        if _platform_ == "linux":
            notify_cmd = "notify-send -a cybld -u critical -t " + str(self.settings.notify_timeout) + \
                         " 'cybld - fail' " + "'" + msg + "'"
        elif _platform_ == "darwin":
            notify_cmd = "osascript -e 'display notification \"" + msg + "\"" + \
                         " with title \"cybld - fail\"'"

        os.system(notify_cmd)

    def _notify_tmux_success(self, msg):
        full_msg = "\"cybld - success: " + msg + "\""
        cybld_tmux_wrapper.CyBldTmuxWrapper.display_message(full_msg)

    def _notify_tmux_fail(self, msg):
        full_msg = "\"cybld - fail: " + msg + "\""
        cybld_tmux_wrapper.CyBldTmuxWrapper.display_message(full_msg)

    def _check_notify(self):
        """ If notifications are enabled, notify-send needs to be available """
        if self.settings.notify_success or self.settings.notify_fail:
            if _platform_ == "linux" and shutil.which("notify-send") is None:
                logging.critical("Notifications enabled, but notify-send not available")
                sys.exit(1)
            # Assume that apples "display notification" is available
