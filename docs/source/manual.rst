Manual
======

Synopsis
--------

``cybld [-h] [-s] [-v] [-c CODEWORD] [-s0 NEWCMD0] [-s1 NEWCMD1] [-s2 NEWCMD2] [{cmd0,cmd1,cmd2}]``

Description
-----------

Trigger commands anywhere. Start without any arguments to start an IPC
server session. Control the server(s) by sending commands.

You can use it to trigger (build) commands in other directories.
It is intended to be used from within editors (vim).

Options
-------

  ``-h``, ``--help``

  ``-v``, ``--version``

  ``-s``, ``--status``

start without any arguments to start a server session

execute commands via positional arguments:

  {*cmd0*, *cmd1*, *cmd2*}

change commands via optional arguments:

  ``-s0`` *NEWCMD0*, ``--newcmd0`` *NEWCMD0*

  ``-s1`` *NEWCMD1*, ``--newcmd1`` *NEWCMD1*

  ``-s2`` *NEWCMD2*, ``--newcmd2`` *NEWCMD2*

send a codeword to only execute the command in certain server sessions:

  ``-c`` *CODEWORD*, ``--codeword`` *CODEWORD*

Usage
-----

Start ``cybld`` in your build folder. It should print the config (i. e.
"python") with which it is running (this determines the commands which will be
executed).

Execute the configured commands by calling ``cybld cmd0``, ``cybld cmd1`` or
``cybld cmd2``.

The configured commands can be (temporarily) changed at runtime by executing
``cybld -s0 <newcommand>``.
This can for example be used to only build and execute one unittest.

Server sessions can be configured to only execute commands if a codeword was
received (``-c <codeword>``). This comes in handy if you keep multiple cybld
sessions open and want to trigger commands based on the current file(type) you are
editing.

Note that server sessions exist within a tmux session. This means that the tmux session
is an implicit codeword by default.

The status of all running IPC server sessions can be queried via
``cybld -s`` (i. e. for statusline display).

Files
-----

*cybld.conf*::

    The main configuration file, containing settings and command groups.
    Will be created at first startup (usually in $HOME/.config).
    The settings section looks like this:

    [settings]
    notify_on_success   = True
    notify_on_fail      = True
    bell_on_success     = False
    bell_on_fail        = True
    notify_timeout      = 3000
    allow_multiple      = True
    print_stats         = True
    talk                = True
    tmux_on_success     = False
    tmux_on_fail        = False
    tmux_refresh_status = False

    Command groups are detected based on the current directory, a file regex and
    the environment variable CYPROJECT and determine the commands which are
    available, i. e.:

    [cpp]
    # Only execute commands if the codeword matches the given codeword regex
    codeword_regex  = .*
    # Query the env variable CYPROJECT
    env_regex  = .*
    # Query the current working directory (full path)
    cwd_regex  = .*
    # Query the environment variable HOSTNAME
    hostname   = .*
    # Query all files in the current directory
    file_regex = CMakeCache.txt
    # First command
    cmd0       = make -j4
    # Second command
    cmd1       = make test
    # Third command
    cmd2       = make clean

    In addition, there are so-called "runner" groups. Such a group essentially
    defines a command:

    [runner_python_tests]
    cmd = python
    param_regex = test_.*.py$

    This will find all files that match the regular expression and call the cmd
    "python" for each of them (i. e. python test_a.py, followed by python
    test_b.py). The exit code (success or failed) is tracked for every command
    executed (and printed in a nice way). Additionally, changes in the exit
    codes are tracked in-between runs (i. e. "test_a.py went BAD" or "test_b.py
    went GOOD").

    The newly defined "runner command can be used by referencing the section
    name:

    # Use the previously defined runner as command
    cmd0 = runner_python_tests

*/tmp/cybld/cybld-ipc-socket*::

    The IPC sockets used for communication between server and client.
    Note that multiple sockets may be open (cybld-ipc-socket-a, cybld-ipc-socket-b,
    and so on).

*.vimrc*::

    The following mappings can be used to trigger commands from within vim (add
    to your .vimrc or similar):

    command! -nargs=1 Silent
    \ | execute ':silent !'.<q-args>
    \ | execute ':redraw!'

    noremap <F7> :Silent cybld cmd0<cr>
    noremap <F8> :Silent cybld cmd1<cr>
    noremap <F9> :Silent cybld cmd2<cr>

    You can use the current file as codeword:

    noremap <F7> :Silent cybld cmd0 -c %:p<cr>
    noremap <F8> :Silent cybld cmd1 -c %:p<cr>
    noremap <F9> :Silent cybld cmd2 -c %:p<cr>

*.bashrc*::

    You can specify the CYPROJECT you are working on and start the cybld server
    instance in one command like this:

    alias foo_cybld = export CYPROJECT="foo"; cybld
    alias bar_cybld = export CYPROJECT="bar"; cybld

    This is for example useful if you have only one build folder, but use
    different build targets depending on which project or task you are currently
    working on.

*.tmux.conf*::

    You can display the status (in progress or the last exit code) in the tmux statusline
    in the following way:

    set -g status-right '#(cybld -s)  #H'

    If the config setting "tmux_refresh_status" is turned on, cybld will automatically
    refresh the tmux statusline whenever the status changes.

Environment
-----------

*CYPROJECT*::

    Determines which commands are loaded for the IPC server. Refer to the config
    parameter env_regex.
