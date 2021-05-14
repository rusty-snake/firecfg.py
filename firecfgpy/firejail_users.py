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

"""Access wrapper around firejail.users"""

import logging


class FirejailUsers:
    """Abstract representation of firejails user access database

    See Also: :manpage:`firejail-users(5)`
    """

    DB_PATH = "/etc/firejail/firejail.users"

    def __init__(self) -> None:
        self.users: set[str] = set()

    def read(self) -> None:
        """Add all users from :py:const:`FirejailUsers.DB_PATH` to ``self.users``

        :raises OSError: Everything that can go wrong when reading a file.
        """

        logging.debug("Reading %s", self.DB_PATH)
        with open(self.DB_PATH, "r") as database:
            self.users.union(database.read().split())

    def write(self) -> None:
        """Add all users from ``self.users`` to :py:const:`FirejailUsers.DB_PATH`

        .. warning::
          This function opens :py:const:`FirejailUsers.DB_PATH` in ``w`` mode
          (i.e. this drops all users in it). You must call :py:func:`read` first
          if you want to keep users which are already allowed to use firejail.

        :raises OSError: Everything that can go wrong when reading a file.
        """

        logging.debug("Writing %s", self.DB_PATH)
        with open(self.DB_PATH, "w") as database:
            database.write("\n".join(sorted(self.users)))

    def add(self, user: str) -> None:
        """Add a user

        :param user: Name of the user to add
        :type user: str
        """

        logging.debug("Add '%s' to firejails user access database", user)
        self.users.add(user)

    def remove(self, user: str) -> None:
        """Remove a user

        :param user: Name of the user to remove
        :type user: str
        """

        logging.debug("Remove '%s' from firejails user access database", user)
        self.users.remove(user)

    def clear(self) -> None:
        """Remove all users"""

        logging.debug("Remove all users from firejails user access database")
        self.users.clear()
