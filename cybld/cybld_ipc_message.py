#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

from enum import Enum

# --------------------------------------------------------------------------


class CyBldIpcMessageType(Enum):
    unknown  = 1
    exec_cmd = 2
    set_cmd  = 3

# --------------------------------------------------------------------------


class CyBldIpcMessage:
    """
    Simple command abstraction.

    An instance of this class is serialized via pickle and then sent to the
    IPC socket.
    """

    def __init__(self):
        self._cmd_type = CyBldIpcMessageType.unknown

        self._codeword     = None
        self._cmd_number   = None
        self._setcmd_param = None
        self._nvim_ipc     = None

    @property
    def cmd_type(self) -> CyBldIpcMessageType:
        """
        Getter for the cmd_type.

        :rtype: CyBldIpcMessageType
        :return: The cmd type.
        """
        return self._cmd_type

    @cmd_type.setter
    def cmd_type(self, cmd_type: CyBldIpcMessageType):
        """
        Set the command type.

        :param cmd_type: The command type ("exec" or "set")
        :type cmd_type:  CyBldIpcMessageType
        """
        assert(self.cmd_type == CyBldIpcMessageType.unknown)
        self._cmd_type = cmd_type

    @property
    def cmd_number(self) -> int:
        """
        Return the cmd_number.

        :rtype: int
        :return: The cmd_number.
        """
        return self._cmd_number

    @cmd_number.setter
    def cmd_number(self, cmd_number: int):
        """
        Set the command number (0, 1 or 2). This is valid for both "set" and
        "exec" commands.

        :param cmd_number: The command number
        :type cmd_number:  int
        """
        assert(self._cmd_number is None)
        assert(cmd_number is 0 or cmd_number is 1 or cmd_number is 2)
        self._cmd_number = cmd_number

    @property
    def setcmd_param(self) -> str:
        """
        Getter for the setcmd_param.

        :rtype: str
        :return: The setcmd_param.
        """
        return self._setcmd_param

    @setcmd_param.setter
    def setcmd_param(self, setcmd_param: str):
        """
        Set the (setcmd) command param (the new command). This is only valid for
        "set" commands.

        :param setcmd_param: The new command string
        :type setcmd_param:  str
        """
        assert(self._setcmd_param is None)
        assert(self.cmd_type == CyBldIpcMessageType.set_cmd)
        self._setcmd_param = setcmd_param

    @property
    def codeword(self) -> str:
        """
        Getter for the codeword.

        :rtype: str
        :return: The codeword.
        """
        return self._codeword

    @codeword.setter
    def codeword(self, codeword: str):
        """
        Set the codeword for the given command.

        :param codeword: The codeword.
        :type codeword:  str
        """
        assert(self._codeword is None)
        self._codeword = codeword

    @property
    def nvim_ipc(self) -> str:
        """
        Getter for the nvim ipc path.

        :rtype: str
        :return: The nvim ipc path.
        """
        return self._nvim_ipc

    @nvim_ipc.setter
    def nvim_ipc(self, nvim_ipc: str):
        """
        Set the nvim ipc path to the given path.

        :param nvim_ipc: The nvim ipc path.
        :type nvim_ipc: str
        """
        assert(self._nvim_ipc is None)
        self._nvim_ipc = nvim_ipc
