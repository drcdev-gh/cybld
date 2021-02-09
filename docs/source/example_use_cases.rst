Example Use-Cases
=================

NeoVim Integration in tmux split
--------------------------------

The picture below shows the integration with NeoVim and tmux:

* command ``tox`` is triggered via a vim mapping
* ``tox`` is executed in the right pane
* once the command has finished, the output is loaded into the quickfix window
* the upper right corner of the tmux statusline shows the exit status of the
  last executed cybld command

.. image:: _pictures/nvim_tmux.png

The corresponding config snippets look like this:

**vimrc**::

    command! -nargs=1 Silent
    \ | execute ':silent !'.<q-args>
    \ | execute ':redraw!'

    noremap <leader>7 :Silent cybld cmd0 -c %<cr>

**tmux.conf**::

    set -g status-right '#(cybld -s)  #H'

**cybld.conf**::

    [settings]
    tmux_refresh_status = True

    [python]
    file_regex = tox.ini
    cmd0 = tox

Note that neovim needs to be started with a valid socket listener address:
``NVIM_LISTEN_ADDRESS=/tmp/nvim_listener nvim``
