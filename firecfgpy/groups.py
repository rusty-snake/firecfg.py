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

"""Load and access groups

Groups in firecfg.py and the equivalent to firecfg.config in firecfg.
They define which programs should be handled by a firejailer.
"""

import logging
from collections import defaultdict
from os import listdir
from os.path import dirname, expanduser
from os.path import join as join_paths
from typing import TextIO, Union


class Groups:
    """Load and access groups"""

    def __init__(self) -> None:
        self.programs: defaultdict[str, set[str]] = defaultdict(set)

    def __getitem__(self, firejailer_id: str) -> set[str]:
        return self.programs[firejailer_id]

    def _load_group(self, fd: TextIO) -> None:
        """Load a group"""

        for line in fd:
            if line[0] in ("#", "\n"):
                continue
            program, firejailers = line.strip().split("=")
            if not firejailers:
                continue
            for firejailer in firejailers.split(","):
                if firejailer[0] == "!":
                    # logging.debug("Discard '%s' from %s", program, firejailer)
                    self.programs[firejailer[1:]].discard(program)
                else:
                    if firejailer not in self.programs:
                        # typo-catcher
                        logging.info("Found new firejailer-id: %s", firejailer)
                    # logging.debug("Add '%s' to %s", program, firejailer)
                    self.programs[firejailer].add(program)

    def _load_from(self, path: str) -> None:
        """Load all groups at ``path``

        :param path: Path to a directory containing group files.
        :type path: str, PathLike (fixme: mypy?), …
        """

        try:
            for group in sorted(listdir(path)):
                with open(join_paths(path, group)) as fd:
                    self._load_group(fd)
        except FileNotFoundError as err:
            if err.filename == path:
                logging.info("%s seems to be empty.", path)
            else:
                raise

    def load_default(self) -> None:
        """Load default groups"""

        logging.debug("Loading default groups")
        self._load_from(join_paths(dirname(__file__), "groups"))

    def load_system(self) -> None:
        """Load system groups"""

        logging.debug("Loading system groups")
        self._load_from("/etc/firecfg.py/groups")

    def load_user(self) -> None:
        """Load user groups"""

        logging.debug("Loading user groups")
        self._load_from(expanduser("~/.config/firecfg.py/groups"))

    def load_all(self) -> None:
        """Load all groups"""

        self.load_default()
        self.load_system()
        self.load_user()
