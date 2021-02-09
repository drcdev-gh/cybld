#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import pytest
import pickle
from cybld import cybld_ipc_message

# --------------------------------------------------------------------------


class TestCyBldIpcMessage:

    def test_cybld_cmd_exec(self):

        sut = cybld_ipc_message.CyBldIpcMessage()

        assert(sut.cmd_type == cybld_ipc_message.CyBldIpcMessageType.unknown)
        assert(sut.codeword is None)
        assert(sut.cmd_number is None)
        assert(sut.setcmd_param is None)

        sut.cmd_type = cybld_ipc_message.CyBldIpcMessageType.exec_cmd
        assert(sut.cmd_type == cybld_ipc_message.CyBldIpcMessageType.exec_cmd)

        sut.codeword = "mysecret"
        assert(sut.codeword == "mysecret")

    def test_cybld_cmd_set(self):

        sut = cybld_ipc_message.CyBldIpcMessage()

        assert(sut.cmd_type == cybld_ipc_message.CyBldIpcMessageType.unknown)
        assert(sut.codeword is None)
        assert(sut.cmd_number is None)
        assert(sut.setcmd_param is None)

        sut.cmd_type = cybld_ipc_message.CyBldIpcMessageType.set_cmd
        assert(sut.cmd_type == cybld_ipc_message.CyBldIpcMessageType.set_cmd)

        sut.setcmd_param = "newcmd"
        assert(sut.setcmd_param == "newcmd")

        sut.codeword = "mysecret"
        assert(sut.codeword == "mysecret")

    def test_cybld_ipc_message_picke(self):

        sut = cybld_ipc_message.CyBldIpcMessage()

        sut.cmd_type = cybld_ipc_message.CyBldIpcMessageType.set_cmd
        sut.cmd_number = 1
        sut.setcmd_param = "param"
        sut.codeword = "mysecret"

        assert(sut.cmd_type == cybld_ipc_message.CyBldIpcMessageType.set_cmd)
        assert(sut.cmd_number == 1)
        assert(sut.setcmd_param == "param")
        assert(sut.codeword == "mysecret")

        pickled_sut = pickle.dumps(sut)
        restored_sut = pickle.loads(pickled_sut)

        assert(restored_sut.cmd_type == cybld_ipc_message.CyBldIpcMessageType.set_cmd)
        assert(restored_sut.cmd_number == 1)
        assert(restored_sut.setcmd_param == "param")
        assert(restored_sut.codeword == "mysecret")

    def test_cybld_cmd_sanity_checks(self):

        with pytest.raises(Exception) as ex1:
            sut = cybld_ipc_message.CyBldIpcMessage()
            sut.cmd_type = cybld_ipc_message.CyBldIpcMessageType.exec_cmd
            sut.cmd_type = cybld_ipc_message.CyBldIpcMessageType.exec_cmd
        assert 'AssertionError' in str(ex1)

        with pytest.raises(Exception) as ex2:
            sut = cybld_ipc_message.CyBldIpcMessage()
            sut.cmd_type = cybld_ipc_message.CyBldIpcMessageType.exec_cmd
            sut.setcmd_param = "newcmd"
        assert 'AssertionError' in str(ex2)

        with pytest.raises(Exception) as ex3:
            sut = cybld_ipc_message.CyBldIpcMessage()
            sut.codeword = "mysecret"
            sut.codeword = "myothersecret"
        assert 'AssertionError' in str(ex3)
