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

from os import getuid, system

from . import config
from .base_firejailer import BaseFirejailer
from .utils import getenv_or, gen_sources

class DBusServiceFirejailer(BaseFirejailer):
    def __init__(self, groups):
        self.name = "D-Bus service"
        sources = gen_sources(getenv_or("XDG_DATA_DIRS", "/usr/local/share:/usr/share"),
                              "dbus-1/services")
        target = config.prefix + "overrides/share/dbus-1/services/"
        super().__init__(sources, target, kind="dbus-service", groups=groups)

    def after(self):
        if getuid() != 0:
            logging.debug("Reloading dbus.service")
            system("systemctl --user reload dbus.service")
        else:
            logging.debug("Skip reloading of dbus.service, cause running as root")
