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
 * Generate aliases for interactive shells
 * Add $SUDO_USER to firejails user access database
 * TODO: Firejail systemd --user
 * TODO: Firejail dbus-system-service

Install
-------

```
python3 -m pip install git+https://github.com/rusty-snake/firecfg.py.git#egg=firecfg.py
firecfg.py setup
firecfg.py
reboot
```

### Arch Linux

There's an [AUR package](https://aur.archlinux.org/packages/python-firecfg-git/).

You still need to `firecfg.py setup && firecfg.py && reboot` after installing.

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
