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

from os import makedirs, symlink
from re import compile as compile_re
from shutil import which

from . import config

class CreateSymlinks:
    ALLOWED_PATTERN = compile_re("[a-zA-Z0-9_.-]+")
    FIREJAIL_EXEC = "/usr/bin/firejail"

    def __init__(self, groups):
        self.programs = groups.programs["symlink"]
        self.bindir = config.prefix + "overrides/bin/"

    def _is_restricted(self, name):
        return not (name == ".." or not CreateSymlinks.ALLOWED_PATTERN.fullmatch(name))

    def create(self):
        makedirs(self.bindir, 0o0755, True)
        for prg in self.programs:
            if self._is_restricted(prg) is False:
                logging.warning(
                    "Skipping program '%s' because it contains disallowed characters",
                    prg)
                continue
            if which(prg):
                logging.info("Create symlink for %s", prg)
                symlink(CreateSymlinks.FIREJAIL_EXEC, self.bindir + prg)
            else:
                logging.debug("Not creating symlink for %s", prg)
