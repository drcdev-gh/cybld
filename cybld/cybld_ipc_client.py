#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import os
import socket
import pickle

from cybld import cybld_helpers

# --------------------------------------------------------------------------


class CyBldIpcClient:
    """
    Used to send ipc commmands to all running cybld ipc sessions

    Constructor get all currently running cybld ipc instances/sockets
    """

    def __init__(self):
        self.socket_names = cybld_helpers.get_current_socket_names()

    def handle_cmd(self, cmd):
        """
        Send the given command (parsed via pickle) to all running cybld ipc sessions.
        Note that this simply ignores timeouts or other socket exceptions.

        :param cmd: which command to send
        :type cmd:  cybld_ipc_message.CyBldIpcMessage
        """
        for socket_name in self.socket_names:
            try:
                ipc_client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                ipc_client.connect(os.path.join(cybld_helpers.get_base_path(), socket_name))
                ipc_client.send(pickle.dumps(cmd))
                ipc_client.close()

            except:
                pass

# --------------------------------------------------------------------------


def send_cmd(cmd):
    """
    Helper method to send the client request in another process (to avoid
    blocking when we call this from vim)

    :param cmd:     The command to execute.
    :type cmd:      cybld_ipc_message.CyBldIpcMessage
    """
    pid = os.fork()
    if pid == 0:
        ipc_client = CyBldIpcClient()
        ipc_client.handle_cmd(cmd)
    else:
        os._exit(0)
