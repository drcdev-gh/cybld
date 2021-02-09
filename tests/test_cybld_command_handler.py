#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import time
import pytest
from cybld import cybld_command_handler
from cybld import cybld_config_command_group
from cybld import cybld_config_settings
from cybld import cybld_ipc_message

# --------------------------------------------------------------------------

class CyBldCommandHandlerMockedConfig:
    def __init__(self):
        self.command_group = cybld_config_command_group.CyBldConfigCommandGroup(
                "name", "codeword", "env", "cwd", "hostname", "file",
                "exit 0", "exit 1", "cmd2")
        self.runner_configs = []
        self.settings = cybld_config_settings.CyBldConfigSettings(
                True, True, False, False, False, False,
                True, True, True, 5, False)

        self.success_callback_called_counter = 0
        self.fail_callback_called_counter    = 0
        self.success_callback_last_text      = None
        self.fail_callback_last_text         = None

        self.ipc_message_exec            = cybld_ipc_message.CyBldIpcMessage()
        self.ipc_message_exec.cmd_type   = cybld_ipc_message.CyBldIpcMessageType.exec_cmd
        self.ipc_message_exec.cmd_number = 0
        self.ipc_message_exec.codeword   = "codeword"

        self.ipc_message_exec_fail            = cybld_ipc_message.CyBldIpcMessage()
        self.ipc_message_exec_fail.cmd_type   = cybld_ipc_message.CyBldIpcMessageType.exec_cmd
        self.ipc_message_exec_fail.cmd_number = 1
        self.ipc_message_exec_fail.codeword   = "codeword"

    def success_callback(self, text):
        self.success_callback_called_counter = self.success_callback_called_counter + 1
        self.success_callback_last_text      = text

    def fail_callback(self, text):
        self.fail_callback_called_counter = self.fail_callback_called_counter + 1
        self.fail_callback_last_text      = text

# --------------------------------------------------------------------------

class TestCyBldCommandHandler:

    def test_cybld_command_handler_init(self):
        mock = CyBldCommandHandlerMockedConfig()
        sut  = cybld_command_handler.CyBldCommandHandler(
                mock.command_group, mock.runner_configs, mock.settings,
                mock.success_callback, mock.fail_callback)

        assert(sut.command_group    is mock.command_group)
        assert(sut.success_callback == mock.success_callback)
        assert(sut.fail_callback    == mock.fail_callback)
        assert(sut.settings         is mock.settings)
        assert(sut.runner_configs   is mock.runner_configs)
        assert(sut.runners          == [])
        assert(sut.stats            is not None)
        assert(sut.talker           is not None)
        assert(sut.busy             is False)
        assert(sut.shared_status    is not None)

        with pytest.raises(Exception) as ex1:
            cybld_command_handler.CyBldCommandHandler(mock.command_group,
                                                      mock.runner_configs,
                                                      mock.settings, None, None)
        assert 'AssertionError' in str(ex1)

    def test_cybld_command_handler_exec_cmd(self):
        mock = CyBldCommandHandlerMockedConfig()
        sut  = cybld_command_handler.CyBldCommandHandler(
                mock.command_group, mock.runner_configs, mock.settings,
                mock.success_callback, mock.fail_callback)

        sut.handle_incoming_ipc_message(mock.ipc_message_exec)
        # Hacky workaround. handle_incoming_ipc_message starts a thread - wait a bit here
        time.sleep(0.5)
        assert(mock.success_callback_called_counter == 1)
        assert(mock.fail_callback_called_counter    == 0)
        assert(mock.success_callback_last_text is mock.command_group.cmd0)

        sut.handle_incoming_ipc_message(mock.ipc_message_exec)
        time.sleep(0.5)
        assert(mock.success_callback_called_counter == 2)
        assert(mock.fail_callback_called_counter    == 0)
        assert(mock.success_callback_last_text is mock.command_group.cmd0)

        sut.handle_incoming_ipc_message(mock.ipc_message_exec_fail)
        time.sleep(0.5)
        assert(mock.success_callback_called_counter == 2)
        assert(mock.fail_callback_called_counter    == 1)
        assert(mock.success_callback_last_text is mock.command_group.cmd0)
        assert(mock.fail_callback_last_text is mock.command_group.cmd1)
