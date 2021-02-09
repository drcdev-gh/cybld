#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import os
import shutil
import subprocess

# --------------------------------------------------------------------------

class CyBldTmuxWrapper:
    @staticmethod
    def is_tmux_available():
        tmux_binary_exists  = shutil.which("tmux") is not None
        tmux_server_running = subprocess.call("tmux info",
                                              shell=True,
                                              stdout=subprocess.DEVNULL,
                                              stderr=subprocess.DEVNULL)
        return tmux_binary_exists and tmux_server_running == 0

    @staticmethod
    def get_session_name():
        if not CyBldTmuxWrapper.is_tmux_available():
            return None
        return os.popen("tmux display-message -p '#S'").read().strip(" ").strip('\n')

    @staticmethod
    def display_message(msg):
        if not CyBldTmuxWrapper.is_tmux_available():
            return
        os.system("tmux display-message " + msg)

    @staticmethod
    def refresh_client():
        if not CyBldTmuxWrapper.is_tmux_available():
            return
        os.system("tmux refresh-client -S")
