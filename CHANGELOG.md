# Changelog

All notable changes to this project will be documented in this file.
The format is loosely based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/).

## [0.1.3] - 2017-09-24

### Added

- Add Makefile target for reqs-dev
- Add Makefile targets for system-wide requirement installation
- Add coverage and codecov
- Allow alt-installs only of python3 in Makefile

### Fixed

- Don't use sudo in Makefile
- Add MacOS to list of supported OS

### Removed

- Remove nix file
- Remove support for python < 3.4

## [0.1.2] - 2017-09-09

### Added

- Add Makefiles (for cybld itself and sphinx documentation)

### Changed

- Change CHANGELOG docu to "Keep a Changelog" format

### Fixed

- Catch exception in nvim IPC that caused hang
- Fix bug which caused the "setcmd" to not work

## [0.1.1] - 2017-08-18

### Added

- cybld now talks after each command has been executed
- Add travis.yml build
- Provide installation and quickstart in README.md

### Changed

- Remove ANSI color codes before sending output to NeoVim
- Prettify output by using different unicode characters

### Fixed

- Fix notification problems under Linux systems
- Fix issue with process handling under Linux systems
- Fix bug which caused logs not to be forwarded to NeoVim
- Properly cleanup log files intended for NeoVim at shutdown

## [0.1.0] - 2017-08-14

### Changed

- Version bump for GitHub release

## [0.0.15] - 2017-03-30

### Added

- "No sessions running" output for tmux/shared status
- Add additional unittests
- Add nix file

### Fixed

- Fix crash under Linux systems
- Proper cleanup on shutdown / lock handling
- Make compatible with Python < 3.5 again (replace subprocess.run)
- Log ERROR message in case installing man page fails (non-root)

### Removed

- Remove $CFGDIR as possible location for the config file

## [0.0.14] - 2017-02-06

### Changed

- Instance name now is the command group name
- Instances are now grouped by tmux session

### Fixed

- Some cleanup and minor bugfixes

## [0.0.13] - 2016-12-21

### Added

- Optional neovim IPC integration
- Add basic sphinx docu
- Add VERSION file

### Fixed

- Check if tmux is available before executing tmux commands
- Lots of code cleanup
- Cleanup: global access to config, no passing around of parameters

## [0.0.12] - 2016-11-13

### Added

- Add tmux notifications
- Add "tmux_refresh_status" option

### Fixed

- Code tests and cleanup

## [0.0.11] - 2016-11-08

### Added

- Add "status query" functionality for statusline display

### Changed

- Put sockets into /tmp/cybld for easier sharing between containers
- Print some things in bold at startup

## [0.0.10] - 2016-09-15

### Changed

- Replace "start" and "end" icons with ">>" and "<<" characters

### Fixed

- Fix shutil import
- Actually make runners work
- Config errors
- Add enum34 as requirement for python versions < 3.4

## [0.0.9] - 2016-09-05

### Added

- Add basic "runner" facilities
- Add "hostname" regex
- Add "--template xxx" for default templates

### Fixed

- Code Cleanup

## [0.0.8] - 2016-03-22

### Added

- Add "codeword" (filter) regex to command groups
- Code documentation
- First py.test

## [0.0.7] - 2016-03-11

### Added

- Basic Darwin support
- Add talker
- Add env_regex for command group

### Changed

- Use "normal" unicode symbols (instead of font awesome)

### Fixed

- Code cleanup
- Fix bug where multiple instances would be started (all matching command groups)

## [0.0.6] - 2016-03-06

### Added

- Add "cwd_regex" config option to detect command group
- Record stats of previous runs

### Fixed

- setup.py fixes/cleanup

## [0.0.5] - 2016-03-06

### Added

- Add man page
- Add --version
- Print pretty unicode characters on success/fail

### Changed

- Update help text

### Fixed

- Remove configparser from setup.py (included by default now)

### Removed

- Removed sphinx docu

## [0.0.4] - 2016-03-06

### Added

- Add exit/keyboard interrupt handler

### Changed

- Remove dependencies
    - Replace dbus with socket IPC
    - Use console notify-send instead of notification lib

## [0.0.3] - 2016-02-11

### Added

- Print commands at startup
- Keep track and print execution time of commands
- Option to ring the terminal bell when command finishes

### Fixed

- Require specific version of notify
- Cleanup output

## [0.0.2] - 2015-09-20

### Added

- Allow changing commands at runtime
- Add support for multiple dbus instances
- Make notification timeout configurable

### Changed

- Only allow one task at a time

### Fixed

- Catch dbus-timeouts and exceptions to avoid cluttering logs

## [0.0.1] - 2015-09-04

- Initial working version
