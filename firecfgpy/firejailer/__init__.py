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

"""Subpackage for firejailers

A firejailer is a class (with a ``run`` methode) that can firejail something
(e.g. .desktop-files in your menu).
"""

FIREJAIL = "/usr/bin/firejail"


class FireJailer:
    """Base class for all firejailers

    ID
      The id of the firejailer used to identify its group (see :py:class:`firecfgpy.groups.Groups`).
    NAME
      The name of the firejailer (maybe) displayed to the user.
    """

    ID: str = NotImplemented
    NAME: str = NotImplemented

    @classmethod
    def run(cls, programs: set[str], overrides: str) -> None:
        raise NotImplementedError
