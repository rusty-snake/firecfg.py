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
from os import listdir

from . import config

class Groups:
    def __init__(self):
        self.programs = {
            "applications": [],
            "autostart": [],
            "dbus-service": [],
            "symlink": [],
        }

    def loaded(self):
        """Return True if the groups are already loaded"""
        return any(self.programs.values())

    def _load_group(self, group_fd):
        for line in group_fd:
            if line[0] in ("#", "\n"):
                continue
            line = line.strip()
            program, places = line.split("=")
            places = places.split(",")
            for place in self.programs:
                if place in places:
                    self.programs[place].append(program)
                elif f"!{place}" in places and program in self.programs[place]:
                    self.programs[place].remove(program)

    def _load_from(self, prefix):
        try:
            groups = listdir(prefix + "groups")
        except FileNotFoundError:
            logging.debug("Skipping to load groups from {prefix}groups")
            return
        groups.sort()
        for group in groups:
            with open(prefix + "groups/" + group) as group_fd:
                self._load_group(group_fd)

    def reload(self):
        """reload the groups from disk"""
        self._load_from(config.SYSTEM_PREFIX)
        self._load_from(config.USER_PREFIX)

    def load(self):
        """load the groups from disks, if not done yet"""
        if not self.loaded():
            self.reload()
        else:
            logging.debug("Groups are already loaded")
