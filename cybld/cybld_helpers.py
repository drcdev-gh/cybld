#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import os
import sys

from cybld import cybld_tmux_wrapper

# --------------------------------------------------------------------------

CONFIG_FILE_NAME = "cybld.conf"
CONFIG_FOLDERS   = ["~/", "~/.config/", "$XDG_CONFIG_HOME/"]

SOCKET_BASE_NAME  = "cybld-ipc-socket"
ROOT_DIR          = "/tmp/cybld"

SHARED_STATUS_FILE      = "cybld.shared"
SHARED_STATUS_LOCK_FILE = "cybld.shared.lock"

IPC_CMD0       = "cmd0"
IPC_CMD1       = "cmd1"
IPC_CMD2       = "cmd2"

IPC_SETCMD0    = "setcmd0"
IPC_SETCMD1    = "setcmd1"
IPC_SETCMD2    = "setcmd2"

SEPERATOR       = "─"
SEPERATOR_COLOR = '\033[94m'
SUCCESS_COLOR   = '\033[34m'
FAIL_COLOR      = '\033[91m'
BOLD_TEXT       = '\033[1m'

RUNNER_SUCCESS_COLOR = '\033[1;97;44m'
RUNNER_FAIL_COLOR    = '\033[1;97;41m'

COLOR_END       = '\033[0m'

ICON_SUCCESS    = "\u2714"
ICON_FAIL       = "\u2716"

ICON_STATUS_START   = "\u2600"
ICON_STATUS_RUNNING = "\u2615"

ICON_UNKNOWN    = "\u274d"

ICON_START      = ">>"
ICON_END        = "<<"

ENV_KEY         = "CYPROJECT"

CONFIG_RUNNER_INDICATOR = "runner_"

NVIM_LOG_PREFIX = "tmp_cybld_log"

# --------------------------------------------------------------------------

def get_base_path():
    tmux_session = cybld_tmux_wrapper.CyBldTmuxWrapper.get_session_name()
    if tmux_session is None:
        return ROOT_DIR

    return os.path.join(ROOT_DIR, tmux_session)

# --------------------------------------------------------------------------

def get_shared_status_file():
    return os.path.join(get_base_path(), SHARED_STATUS_FILE)

# --------------------------------------------------------------------------

def get_shared_status_lock_file():
    return os.path.join(get_base_path(), SHARED_STATUS_LOCK_FILE)

# --------------------------------------------------------------------------

def get_term_width():
    if sys.stdout.isatty():
        stty_size = os.popen('stty size', 'r').read().split()
        # Safeguard in case .TERM is not set (i.e. py.test)
        if len(stty_size) >= 1:
            return int(stty_size[1])
    return int(180)

# --------------------------------------------------------------------------

def get_current_socket_names():
    """ Get all cybld socket names """
    ret = list()
    for socket_file in os.listdir(get_base_path()):
        if socket_file.startswith(SOCKET_BASE_NAME):
            ret.append(socket_file)
    ret.sort()
    return ret

# --------------------------------------------------------------------------

def print_seperator_lines(lines=2):
    """ Print (two) seperator lines (full width of terminal) """
    width = get_term_width()
    print((SEPERATOR_COLOR + SEPERATOR * width + COLOR_END) * lines)

# --------------------------------------------------------------------------

def print_text_with_bg(text, success_or_fail):
    if success_or_fail is True:
        text = RUNNER_SUCCESS_COLOR + \
               "{:{term_width}} {:>} ".format(text, ICON_SUCCESS,
                                              term_width = get_term_width() - 3) + COLOR_END
    elif success_or_fail is False:
        text = RUNNER_FAIL_COLOR + \
               "{:{term_width}} {:>} ".format(text, ICON_FAIL,
                                              term_width = get_term_width() - 3) + COLOR_END
    else:
        text = "{:{term_width}} {:>} ".format(text, ICON_UNKNOWN,
                                              term_width = get_term_width())

    print(text)

# --------------------------------------------------------------------------

def print_centered_text(text, success_or_fail):
    """
    Print the given text in the center of the terminal (and include start and
    end icons, as well as an icon indicating success or fail). In addition, the
    text is colored depending on "success or failure".

    :param text:    The text to print
    :type text:     str

    :param success_or_fail: Whether we want to indicate success or failure. Set
                            to None to do neither.
    :type success_or_fail:  bool
    """
    if success_or_fail is True:
        text = ICON_START + " " + ICON_SUCCESS + \
               " " + text + " " + ICON_END
    elif success_or_fail is False:
        text = ICON_START + " " + ICON_FAIL + \
               " " + text + " " + ICON_END
    else:
        text = ICON_START + " " + text + " " + ICON_END

    width  = get_term_width()
    spaces = int((width - len(text)) / 2)
    if success_or_fail is True:
        print(" " * spaces + SUCCESS_COLOR + text + COLOR_END)
    elif success_or_fail is False:
        print(" " * spaces + FAIL_COLOR + text + COLOR_END)
    else:
        print(" " * spaces + text)
