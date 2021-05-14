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

"""A list with all firejailer classes (``firecfgpy.firejailer.firejailers.FIREJAILERS``)."""

from .alias import Alias
from .applications import Applications
from .autostart import Autostart
from .dbus_service import DBusService
from .symlink import Symlink

FIREJAILERS = [
    Alias,
    Applications,
    Autostart,
    DBusService,
    Symlink,
]
