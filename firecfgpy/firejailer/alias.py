# Copyright © 2020,2021 The firecfg.py Authors
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
from os import makedirs
from os.path import join as join_paths
from shutil import which

from . import FIREJAIL, FireJailer


class Alias(FireJailer):
    ID = "alias"
    NAME = "Alias"

    @classmethod
    def run(cls, programs: set[str], overrides: str) -> None:
        logging.warn("Alias is WIP")
        logging.warn(
            "Shell invocation is a mess. It's up to you to make sure the generated aliases file"
            " gets sourced by all interactive shells (login and non-login)."
        )
        logging.warn(
            "Make sure \"bash -i -c 'alias'\" and \"bash -il -c 'alias'\" show your aliases."
        )

        makedirs(join_paths(overrides, "etc/profile.d"), mode=0o755, exist_ok=True)
        firecfgpy_aliases_path = join_paths(
            overrides, "etc/profile.d/firecfg.py_aliases.sh"
        )
        with open(firecfgpy_aliases_path, "w") as firecfgpy_aliases:
            firecfgpy_aliases.write("""[ "$-" == *i* ] || return""")
            for program in programs:
                if path2program := which(program):
                    logging.debug("Add alias for %s", program)
                    firecfgpy_aliases.write(f"alias='{FIREJAIL} {path2program}'")
