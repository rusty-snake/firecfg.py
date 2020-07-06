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

class _BaseFixer:
    """A fixer can fix excatly one problematic thing in a desktop file

    KIND: The type of the fixer consisting of two parts, spearted by a ':'
        1. 'general' or 'special'
        2. 'autostart', 'applications' or 'dbus-service'
    FILES: If this is a special fixer, the name of the file must match one of the given regexp.
    """
    #KIND = "(general|special):(autostart|applications|dbus-service)"
    KIND = ""
    FILES = []

    def can_fix(self, context, line):
        """This function is called for _every_ line in the file,
        and should give a quick answer whether this fixer can probably fix it.
        :param context: {
            "source_dir": "/usr/share/applications/",
            "source_file_name": "firefox.desktop",
            "source_file_path": "/usr/share/applications/firefox.desktop",
            "target_file_path": "/etc/firecfg.py/overrides/share/applications/firefox.desktop",
            "program_name": "firefox",
            "section": "Desktop Entry",
        }
        :param line: {
            "key": "Exec",
            "value": "firefox %u",
            "rawline": "Exec=firefox %u",
        }
        :retruns: True if `fix` can likely fix this line.
        """
        return False

    def fix(self, context, line):
        """Correct the line
        :param context: same as can_fix
        :param line: same as can_fix
        :returns: The fixed (or unchanged) line
        """
        return line["rawline"]


####################

class PrependUsrBinFirejailOnAbsoluteExec(_BaseFixer):
    def can_fix(self, context, line):
        return line["key"] == "Exec" and line["value"][0] == "/"

    def fix(self, context, line):
        return "Exec=/usr/bin/firejail " + line["value"]


class PUBFOAE_Autostart(PrependUsrBinFirejailOnAbsoluteExec):
    KIND = "general:autostart"


class PUBFOAE_Applications(PrependUsrBinFirejailOnAbsoluteExec):
    KIND = "general:applications"


class PUBFOAE_DBusService(PrependUsrBinFirejailOnAbsoluteExec):
    KIND = "general:dbus-service"


####################

FIXERS = [
    PUBFOAE_Autostart(),
    PUBFOAE_Applications(),
    PUBFOAE_DBusService(),
]
