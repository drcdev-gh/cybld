#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------

class CyBldConfigSettings:
    def __init__(self, notify_success, notify_fail,
                 bell_success, bell_fail,
                 tmux_success, tmux_fail,
                 allow_multiple, print_stats, talk,
                 notify_timeout, tmux_refresh_status):

        self.notify_success      = notify_success
        self.notify_fail         = notify_fail
        self.bell_success        = bell_success
        self.bell_fail           = bell_fail
        self.tmux_success        = tmux_success
        self.tmux_fail           = tmux_fail
        self.allow_multiple      = allow_multiple
        self.print_stats         = print_stats
        self.talk                = talk
        self.notify_timeout      = notify_timeout
        self.tmux_refresh_status = tmux_refresh_status
