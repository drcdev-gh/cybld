#!/usr/bin/python

# --------------------------------------------------------------------------
#
# MIT License
#
# --------------------------------------------------------------------------

import argparse
import logging
import sys
import os

# Need to setup logging before imports
# Python lets a random library (neovim) eat my log output otherwise
logging.basicConfig(format = '%(asctime)s %(message)s', level = logging.INFO,
                    datefmt='%H:%M:%S')

import cybld.cybld_config_command_group                     # noqa: E402
from cybld.cybld_config_settings import CyBldConfigSettings # noqa: E402
from cybld import cybld_ipc_message                         # noqa: E402
from cybld import cybld_ipc_client                          # noqa: E402
from cybld import cybld_config                              # noqa: E402
from cybld import cybld_helpers                             # noqa: E402
from cybld import cybld_ipc_server                          # noqa: E402
from cybld import cybld_templates                           # noqa: E402
from cybld.cybld_shared_status import CyBldSharedStatus     # noqa: E402
from cybld.cybld_config_runner import CyBldConfigRunner     # noqa: E402

# --------------------------------------------------------------------------

def get_version():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../VERSION')) as version_file:
        return version_file.read().strip()
    return "unknown"

# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="cybld - trigger commands anywhere.\n" +
                                     "Start without any arguments to start an IPC server session. " +
                                     "Control the server(s) by sending commands.",
                                     epilog="For more information, RTFM.")
    parser.add_argument("-v", '--version', action='version', version='%(prog)s ' + get_version())
    parser.add_argument("-t", '--templates', help='List available templates',
                        action="store_true")
    parser.add_argument("-a", '--addtemplate', help='Add a template to the config file')
    parser.add_argument("-s", '--status', help='Print the status of running IPC instances (i. e. for status line)',
                        action="store_true")

    clt_parser    = parser.add_argument_group("client arguments", "Arguments available only to the client. " +
                                              "One argument is required (otherwise a server session is started).")
    clt_parser.add_argument("-c", "--codeword",
                            help="Only execute the command on command groups which codeword_fliter matches the "
                            " given codeword (default string is DEFAULT)", default="DEFAULT")
    clt_ex_parser = clt_parser.add_mutually_exclusive_group(required = False)
    clt_ex_parser.add_argument("cmd", nargs="?", help="command to execute",
                               choices=["cmd0", "cmd1", "cmd2"])
    clt_ex_parser.add_argument("-s0", "--newcmd0", help="change command 0")
    clt_ex_parser.add_argument("-s1", "--newcmd1", help="change command 1")
    clt_ex_parser.add_argument("-s2", "--newcmd2", help="change command 2")

    args = parser.parse_args()

    if args.status:
        shared_status = CyBldSharedStatus(True)
        shared_status.print_pretty()
        exit(0)

    handle_templates(args)

    if not os.path.isdir(cybld_helpers.get_base_path()):
        os.makedirs(cybld_helpers.get_base_path())

    if not len(sys.argv) > 1:
        handle_ipc_server()

    else:
        handle_ipc_client(args)


def handle_ipc_client(args):
    my_cmd = cybld_ipc_message.CyBldIpcMessage()
    if args.cmd:
        my_cmd.cmd_type = cybld_ipc_message.CyBldIpcMessageType.exec_cmd

        if args.cmd == cybld_helpers.IPC_CMD0:
            my_cmd.cmd_number = 0
        elif args.cmd == cybld_helpers.IPC_CMD1:
            my_cmd.cmd_number = 1
        elif args.cmd == cybld_helpers.IPC_CMD2:
            my_cmd.cmd_number = 2
        else:
            assert (False)
    else:
        my_cmd.cmd_type = cybld_ipc_message.CyBldIpcMessageType.set_cmd
        if args.newcmd0:
            my_cmd.cmd_number = 0
            my_cmd.setcmd_param = args.newcmd0
        elif args.newcmd1:
            my_cmd.cmd_number = 1
            my_cmd.setcmd_param = args.newcmd1
        elif args.newcmd2:
            my_cmd.cmd_number = 2
            my_cmd.setcmd_param = args.newcmd2
    my_cmd.codeword = args.codeword
    my_cmd.nvim_ipc = os.getenv('NVIM_LISTEN_ADDRESS', "")
    cybld_ipc_client.send_cmd(my_cmd)


def handle_ipc_server():
    config = cybld_config.CyBldConfig()
    found_matching_group = False
    for command_group_section in config.get_command_groups():
        command_group = cybld.cybld_config_command_group.CyBldConfigCommandGroup(command_group_section,
                                                                                 config.get_command_group_codeword_regex(
                                                                                     command_group_section),
                                                                                 config.get_command_group_env_regex(
                                                                                     command_group_section),
                                                                                 config.get_command_group_cwd_regex(
                                                                                     command_group_section),
                                                                                 config.get_command_group_hostname_regex(
                                                                                     command_group_section),
                                                                                 config.get_command_group_file_regex(
                                                                                     command_group_section),
                                                                                 config.get_command_group_cmd0(
                                                                                     command_group_section),
                                                                                 config.get_command_group_cmd1(
                                                                                     command_group_section),
                                                                                 config.get_command_group_cmd2(
                                                                                     command_group_section))

        if (command_group.env_regex_matches() and command_group.file_regex_matches() and
                command_group.cwd_regex_matches() and command_group.hostname_regex_matches()):
            found_matching_group = True
            cybld_ipc_server.CyBldIpcServer(command_group,
                                            transform_runners(config),
                                            transform_config_settings(config))

            # Only load first command group
            break
    if not found_matching_group:
        logging.critical("No matching command group found - Adapt your config (" +
                         config.configfile + ")!")
        sys.exit(1)


def handle_templates(args):
    if args.templates:
        print("Available templates are: " + ", ".join(cybld_templates.templates.keys()))
        exit(0)
    if args.addtemplate:
        if args.addtemplate not in cybld_templates.templates.keys():
            logging.error("Template " + args.addtemplate + " is not available.")
            exit(1)

        config = cybld_config.CyBldConfig()
        config.add_command_group(cybld_templates.templates[args.addtemplate])
        exit(0)

def transform_config_settings(config):
    return CyBldConfigSettings(config.get_notify_success(), config.get_notify_fail(),
                               config.get_bell_success(),   config.get_bell_fail(),
                               config.get_tmux_success(),   config.get_tmux_fail(),
                               config.get_allow_multiple(), config.get_print_stats(),
                               config.get_talk(),           config.get_notify_timeout(),
                               config.get_tmux_refresh_status())


def transform_runners(config):
    transformed_configs = []
    for config_runner in config.get_runners():
        transformed_runner = CyBldConfigRunner(config_runner,
                                               config.get_runner_command(config_runner),
                                               config.get_runner_regex_find_params(config_runner))
        transformed_configs.append(transformed_runner)

    return transformed_configs


if __name__ == "__main__":
    main()
