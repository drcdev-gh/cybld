# cybld - trigger commands anywhere
[![Build Status](https://travis-ci.org/drcdev-gh/cybld.svg?branch=master)](https://travis-ci.org/drcdev-gh/cybld) [![codecov](https://codecov.io/gh/drcdev-gh/cybld/branch/master/graph/badge.svg)](https://codecov.io/gh/drcdev-gh/cybld) [![Code Climate](https://codeclimate.com/github/drcdev-gh/cybld/badges/gpa.svg)](https://codeclimate.com/github/drcdev-gh/cybld)

cybld is a developer tool that can be used to trigger commands in another terminal via IPC
(e. g. from an editor). The commands are configurable based on a number of things, such
as the hostname or the current working directory.
It also features integration with NeoVim and tmux and provides helpers to support better
local testing.

## Installation

cybld runs under MacOS or Linux systems and requires Python 3.

```
git clone git@github.com:drcdev-gh/cybld.git
cd cybld

# Install optional dependencies if wanted
make reqs

# Install cybld
make install
```

## Quickstart

```
# Run cybld somewhere in order to create the empty configfile
cybld
# Add a template for your programming language of choice to the configfile
cybld --addtemplate python
```

Then configure the commands as needed.

```
# Start the server session in the folder you want to execute the commands in
cybld
# From another terminal, trigger command 0
cybld cmd0
```

The full man page is available in the docs folder: [docs/source/manual.rst](docs/source/manual.rst).
