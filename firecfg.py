#!/usr/bin/python3 -I

# Copyright © 2020 rusty-snake
#
# This file is part of firecfg.py
#
# firecfg.py is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# firecfg.py is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

import logging
from os import getuid
from shutil import rmtree

from firecfg import config
from firecfg.groups import Groups
from firecfg.create_symlinks import CreateSymlinks
from firecfg.autostart_firejailer import AutostartFirejailer
from firecfg.applications_firejailer import ApplicationsFirejailer
from firecfg.dbus_service_firejailer import DBusServiceFirejailer

def main():
    logging.basicConfig(
        format="firecfg.py:%(levelname)s: %(message)s",
        level=logging.INFO if not config.DEBUG else logging.DEBUG,
        )

    if getuid() == 0:
        config.prefix = config.SYSTEM_PREFIX
    else:
        config.prefix = config.USER_PREFIX

    groups = Groups()
    groups.load()

    try:
        rmtree(config.prefix + "overrides")
    except FileNotFoundError as err:
        if err.filename != config.prefix + "overrides":
            raise

    CreateSymlinks(groups).create()
    AutostartFirejailer(groups).firejail()
    ApplicationsFirejailer(groups).firejail()
    DBusServiceFirejailer(groups).firejail()

if __name__ == "__main__":
    main()
