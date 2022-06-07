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

from .common import PrependFirejailInExecKeys


class DBusService(PrependFirejailInExecKeys):
    ID = "dbus-service"
    NAME = "D-Bus service"

    SOURCES_ENV = "XDG_DATA_DIRS"
    SOURCES_DEFAULT = "/usr/local/share:/usr/share"
    SOURCES_SUBDIR = "dbus-1/services"
    TARGET_SUFFIX = "data/dbus-1/services"
