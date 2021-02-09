#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

from cybld import cybld_ipc_neovim

# --------------------------------------------------------------------------

class TestCyBldIpcNeovim:

    @staticmethod
    def get_cybld_ipc_neovim_instance():
        return cybld_ipc_neovim.CyBldIpcNeovim(True, "/tmp/cybld/tstipcneovim",
                                               "/tmp/cybld/tstipcneovim_log", "make -j4")

    def test_init(self):
        sut = TestCyBldIpcNeovim.get_cybld_ipc_neovim_instance()

        assert(sut._enabled is True)
        assert(sut._ipc_socket_path == "/tmp/cybld/tstipcneovim")
        assert(sut._logfile_path    == "/tmp/cybld/tstipcneovim_log")
        assert(sut._command         == "make -j4")

    def test_should_do_ipc(self):
        sut = TestCyBldIpcNeovim.get_cybld_ipc_neovim_instance()
        assert(sut._should_do_ipc is True)

    def test_should_do_no_ipc_command(self):
        sut          = TestCyBldIpcNeovim.get_cybld_ipc_neovim_instance()
        sut._command = "random"
        assert(sut._should_do_ipc is False)

    def test_should_do_no_ipc_socket(self):
        sut                  = TestCyBldIpcNeovim.get_cybld_ipc_neovim_instance()
        sut._ipc_socket_path = None
        assert(sut._should_do_ipc is False)
