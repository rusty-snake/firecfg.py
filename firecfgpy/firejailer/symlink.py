# Copyright © 2020-2022 The firecfg.py Authors
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
from os.path import join as join_paths
from shutil import which

from . import FIREJAIL, FireJailer


class Symlink(FireJailer):
    ID = "symlink"
    NAME = "Symlink"

    @classmethod
    def run(cls, programs: set[str], overrides: str) -> None:
        bindir = join_paths(overrides, "bin")
        makedirs(bindir, 0o0755, exist_ok=True)

        for program in programs:
            if which(program):
                logging.debug("Create symlink for %s", program)
                symlink(FIREJAIL, join_paths(bindir, program))
