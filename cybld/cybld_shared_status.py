#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

from contextlib import contextmanager
from enum import Enum

import atexit
import logging
import os
import pickle
import random
import string
import sys
import time

from cybld import cybld_helpers
from cybld import cybld_tmux_wrapper

# --------------------------------------------------------------------------

class CyBldIpcServerStatus(Enum):
    started = 1
    running = 2
    success = 3
    fail    = 4

class CyBldSharedStatus():

    def __init__(self, read_only, name = None, tmux_refresh_status = False):
        self.status_map = {}
        self.read_only           = read_only
        self.tmux_refresh_status = tmux_refresh_status

        # Ensure that the folder exists...
        try:
            os.makedirs(cybld_helpers.get_base_path())
        except:
            pass

        self.read()

        if self.read_only is False:
            assert(name is not None)
            self.name = self.generate_name_with_random_postfix(name)

            logging.info("Name of this instance is " + cybld_helpers.BOLD_TEXT +
                         self.name + cybld_helpers.COLOR_END)
            atexit.register(self.shutdown)
            self.set_started()

    @contextmanager
    def _lock(self, release=True):
        self.try_lock()
        self.read()
        try:
            yield
        finally:
            self.write()
            if release:
                self.release_lock()

    def set_started(self):
        with self._lock():
            self.status_map[self.name] = CyBldIpcServerStatus.started

    def set_running(self):
        with self._lock():
            self.status_map[self.name] = CyBldIpcServerStatus.running

    def set_success(self):
        with self._lock():
            self.status_map[self.name] = CyBldIpcServerStatus.success

    def set_fail(self):
        with self._lock():
            self.status_map[self.name] = CyBldIpcServerStatus.fail

    def read(self):
        if os.path.isfile(cybld_helpers.get_shared_status_file()):
            shared_status_file = open(cybld_helpers.get_shared_status_file(), "rb")
            self.status_map = pickle.load(shared_status_file)
            shared_status_file.close()

    def write(self):
        if self.read_only:
            logging.critical("Cannot write in read only mode. Call a code monkey.")
            sys.exit(1)

        shared_status_file = open(cybld_helpers.get_shared_status_file(), "wb+")
        pickle.dump(self.status_map, shared_status_file)
        shared_status_file.close()

        if self.tmux_refresh_status:
            cybld_tmux_wrapper.CyBldTmuxWrapper.refresh_client()

    # TODO DC: write the process uid in the shared status lock file to detect stale files?
    def try_lock(self):
        while os.path.isfile(cybld_helpers.get_shared_status_lock_file()):
            time.sleep(1)

        try:
            lock_file = open(cybld_helpers.get_shared_status_lock_file(), 'x')
            lock_file.close()
        except:
            self.try_lock()

    def release_lock(self):
        os.remove(cybld_helpers.get_shared_status_lock_file())

    def print_pretty(self):
        pretty_string = ""
        for key, value in sorted(self.status_map.items()):
            if len(pretty_string) != 0:
                pretty_string += " | "

            pretty_string += key + ":"
            if value is CyBldIpcServerStatus.started:
                pretty_string += cybld_helpers.ICON_STATUS_START
            elif value is CyBldIpcServerStatus.running:
                pretty_string += cybld_helpers.ICON_STATUS_RUNNING
            elif value is CyBldIpcServerStatus.success:
                pretty_string += cybld_helpers.ICON_SUCCESS
            elif value is CyBldIpcServerStatus.fail:
                pretty_string += cybld_helpers.ICON_FAIL
            else:
                pretty_string += cybld_helpers.ICON_UNKNOWN

        if len(pretty_string) == 0:
            pretty_string = "no cybld session running"

        print(pretty_string)

    def shutdown(self):
        with self._lock(False):
            try:
                del self.status_map[self.name]
            except:
                pass

        if len(self.status_map) == 0:
            logging.info("Removing shared status file...")
            os.remove(cybld_helpers.get_shared_status_file())

        self.release_lock()

    def generate_name_with_random_postfix(self, name):
        choices = ["Taengoo", "Sica", "Soonkyu", "Tippany", "Hyo",
                   "Yul", "Soo", "Yoong", "Seororo"]
        random.shuffle(choices)

        for choice in choices:
            name_and_postfix = name + " [" + choice + "]"
            if name_and_postfix not in self.status_map:
                return name_and_postfix

        # Generate random gibberish as fallback
        gibberish = ""
        while True:
            gibberish += "".join(random.sample(string.ascii_uppercase, 1))
            if len(gibberish) == 5:
                break

        name_and_gibberish = name + " [" + gibberish + "]"
        return name_and_gibberish
