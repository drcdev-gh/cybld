#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import atexit
import logging
import os
import pty
import subprocess
import tempfile
import threading
import time
import termios
import errno
import re

from cybld import cybld_command_stats, cybld_talker, cybld_ipc_message, cybld_helpers
from cybld.cybld_config_command_group import CyBldConfigCommandGroup
from cybld.cybld_config_runner import CyBldConfigRunner
from cybld.cybld_config_settings import CyBldConfigSettings
from cybld.cybld_ipc_message import CyBldIpcMessage
from cybld.cybld_ipc_neovim import CyBldIpcNeovim
from cybld.cybld_runner import CyBldRunner
from cybld.cybld_shared_status import CyBldSharedStatus

# --------------------------------------------------------------------------

class CyBldCommandHandler:
    """
    Helper class to set and execute commands.

    Some notes:
        - Commands are executed in a seperate thread and only
          one command can be executed at any given time (busy flag)
        - Commands can be changed while a command is running (not protected
          by busy flag)

    :param command_group:    Refer to CyBldConfigCommandGroup.

    :param runner_configs:   All parsed runner configs.

    :param settings:         Refer to CyBldConfigSettings.

    :param success_callback: Which function (i. e. notify success) to call
                             when the command returned 0.
    :param fail_callback:    Which function (i. e. notify fail) to call
                             when the command returned not 0 or if we
                             are busy.
    """

    def __init__(self, command_group: CyBldConfigCommandGroup,
                 runner_configs, settings: CyBldConfigSettings,
                 success_callback, fail_callback):
        assert success_callback is not None
        assert fail_callback is not None

        self.command_group    = command_group
        self.success_callback = success_callback
        self.fail_callback    = fail_callback
        self.settings         = settings

        self.runner_configs  = runner_configs
        self.runners         = []
        self._initialize_runners_startup()

        self.stats            = cybld_command_stats.CyBldCommandStatsList()
        self.talker           = cybld_talker.CyBldTalker(settings.talk)

        self.busy             = False

        self.shared_status = CyBldSharedStatus(False, self.command_group.name,
                                               settings.tmux_refresh_status)
        self.talker.say_hello()
        atexit.register(self.talker.say_goodbye)

    def _initialize_runners_startup(self):
        """
        Initialize the runner configs in case a command matches a configured
        runner.
        """
        if self.command_group.is_cmd0_runner():
            self._initialize_runner(self.command_group.cmd0)
        if self.command_group.is_cmd1_runner():
            self._initialize_runner(self.command_group.cmd1)
        if self.command_group.is_cmd2_runner():
            self._initialize_runner(self.command_group.cmd2)

    def _initialize_runner(self, runner_name: str):
        """
        Helper method to initialize a given runner.
        Note that a runner with the given name must exist (assert).

        :param runner_name: The name of the runner which should be initialized.
        """
        # Runner already loaded
        for runner in self.runners:
            if runner.config.name == runner_name:
                return

        # Find the runner config with the name
        valid_runner_config = None
        for runner_config in self.runner_configs:
            if runner_config.name == runner_name:
                valid_runner_config = runner_config
                break

        assert isinstance(valid_runner_config, CyBldConfigRunner)
        runner = CyBldRunner(valid_runner_config)
        self.runners.append(runner)

    def handle_incoming_ipc_message(self, ipc_message: CyBldIpcMessage):
        """
        Handle the incoming message by calling exec_cmd.
        Note that this quits immediately in case the codeword is invalid.

        :param ipc_message: The incoming command.
        """
        if not self.command_group.codeword_regex_matches(ipc_message.codeword):
            return

        if ipc_message.cmd_type == cybld_ipc_message.CyBldIpcMessageType.set_cmd:
            self._change_cmd(ipc_message.cmd_number, ipc_message.setcmd_param)
        elif ipc_message.cmd_type == cybld_ipc_message.CyBldIpcMessageType.exec_cmd:
            self._exec_cmd(ipc_message.cmd_number, ipc_message.nvim_ipc)
        else:
            assert False

    def _change_cmd(self, cmd_number: int, new_cmd: str):
        """
        Change the command cmd (cmd0, cmd1, cmd2) to new_cmd

        :param cmd_number: The cmd_number which should be changed
        :param new_cmd:    The string of the new command
        """
        if cmd_number is 0:
            self.command_group.cmd0 = str(new_cmd)
        elif cmd_number is 1:
            self.command_group.cmd1 = str(new_cmd)
        elif cmd_number is 2:
            self.command_group.cmd2 = str(new_cmd)
        else:
            assert False

        if self.command_group.is_cmd_runner_command(new_cmd):
            self._initialize_runner(new_cmd)

        logging.info("Setting {0} to {1}".format(str(cmd_number), str(new_cmd)))
        cybld_helpers.print_seperator_lines()

    def _exec_cmd(self, cmd_number: int, nvim_ipc: str):
        """
        Execute the given command in a new thread (if we aren't busy)

        :param cmd_number: The command number which should be executed
        :param nvim_ipc:   The NVIM IPC name, if available
        """
        # TODO: give the option to kill the existing task instead
        if self.busy is True:
            self.fail_callback("currently busy")
            return

        cmd_translated = None
        if cmd_number is 0:
            cmd_translated = self.command_group.cmd0
        elif cmd_number is 1:
            cmd_translated = self.command_group.cmd1
        elif cmd_number is 2:
            cmd_translated = self.command_group.cmd2

        if cmd_translated is not None:
            task = threading.Thread(target = self._exec_cmd_helper, args = (cmd_translated,
                                                                            nvim_ipc,))
            task.start()
        else:
            assert False

    def _exec_cmd_helper(self, cmd: str, nvim_ipc: str):
        """
        Helper function to execute the given command and call the success/fail callbacks

        :param cmd:         The command (full string) which should be executed
        :param nvim_ipc:    The NVIM IPC name, if available
        """
        assert self.busy is False

        self.shared_status.set_running()
        self.busy = True
        os.system("clear")
        logging.info("Executing cmd {0}".format(cmd))

        start = time.time()

        success = False
        if self.command_group.is_cmd_runner_command(cmd):
            for runner in self.runners:
                if runner.config.name == cmd:
                    success = runner.run_all()
                    break
        else:
            # The code block below essentially just "tees" the stdout and
            # stderr to a log file, while still preserving the terminal
            # output (inclusive colors).
            # Using subprocess.PIPE does not seem possible under Darwin,
            # since the pipe does not have the isatty flag set (the isatty
            # flag affects the color output).
            # Note that the file is only written at the end and not streamed.
            master, slave = pty.openpty()

            # This prevents LF from being converted to CRLF
            attr = termios.tcgetattr(slave)
            attr[1] = attr[1] & ~termios.ONLCR
            termios.tcsetattr(slave, termios.TCSADRAIN, attr)

            proc = subprocess.Popen(cmd, shell=True, stdout=slave, stderr=slave, close_fds=False)

            # Close the write end of the pipe in this process, since we don't need it.
            # Otherwise we would not get EOF etc.
            os.close(slave)

            read_stdout_stderr = os.fdopen(master, 'rb', buffering=0)
            complete_output    = ""

            try:
                while proc.poll() is None:
                    output = read_stdout_stderr.readline()
                    os.write(1, output)
                    complete_output += output.decode()

                # Read the last line
                output = read_stdout_stderr.readline()
                os.write(1, output)
                complete_output += output.decode()
            # This error is "expected" under Linux systems.
            # readline() doesn't seem to behave properly there.
            # The exception does not occur on MacOS.
            except OSError as oserr:
                if oserr.errno != errno.EIO or proc.poll() is None:
                    logging.critical("Unexpected OS error: {0}".format(oserr))
            except:
                logging.critical("Unexpected error while reading from process")

            os.close(master)
            proc.wait()

            if proc.returncode == 0:
                success = True

            logfile, logfilename = tempfile.mkstemp(dir=cybld_helpers.get_base_path(),
                                                    prefix=cybld_helpers.NVIM_LOG_PREFIX)

            # strip color codes from logfile
            # complete_output = re.sub(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]', '', complete_output)
            complete_output = re.sub(r'\x1b(\[.*?[@-~]|\].*?(\x07|\x1b\\))', '', complete_output)

            with open(logfile, 'w+') as logfile_opened:
                logfile_opened.write(complete_output)

            CyBldIpcNeovim(True, nvim_ipc, logfilename, cmd)

        end = time.time()

        self.busy = False
        cybld_helpers.print_seperator_lines()

        timediff_in_seconds = str(int(end - start))

        if success:
            cybld_helpers.print_centered_text("SUCCESS: {0} ({1} seconds)".format(cmd, timediff_in_seconds), True)
            self.shared_status.set_success()
        else:
            cybld_helpers.print_centered_text("FAIL: {0} ({1} seconds)".format(cmd, timediff_in_seconds), False)
            self.shared_status.set_fail()

        if self.settings.print_stats:
            cybld_helpers.print_centered_text(self.stats.get_command_stats(cmd), None)

        if success:
            self.talker.say_success()
        else:
            self.talker.say_fail()

        cybld_helpers.print_seperator_lines()
        self.stats.update_command_stats(cmd, success, int(timediff_in_seconds))

        if success:
            self.success_callback(cmd)
        else:
            self.fail_callback(cmd)
