firecfg.py
==========

[![maintenance-status: experimental](https://img.shields.io/badge/maintenance--status-experimental-orange)](https://gist.github.com/rusty-snake/574a91f1df9f97ec77ca308d6d731e29)

An improved firecfg written in python.

Features
--------

 * Firejail $PATH (symlink)
 * Firejail applications (aka .desktop-files)
 * Firejail dbus-services
 * Firejail autostart
 * Add $SUDO_USER to firejails user access database
 * TODO: Firejail systemd --user
 * TODO: Firejail dbus-system-service
 * TODO: bashrc aliases for interactive shells

FAQ
---

### I want to be warned about wrong setups.

Add this to your .bashrc:

```bash
if [[ :$PATH: != *:/etc/firecfg.py/overrides/bin:* ]]; then
    echo 'WARNING: firecfg.py in not in $PATH!'
fi
```

License
-------

GPL-3.0-or-later
