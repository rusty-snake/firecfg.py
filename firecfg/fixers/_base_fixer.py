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
    """A fixer can fix excatly one problematic thing in a desktop file"""

    def can_fix(self, context, line):
        """This function is called for _every_ line in the desktop file,
        and should give a quick answer whether this fixer can probably fix it.
        :param context: {
            "filename": "firefox.desktop",
            "program": "firefox",
            "section": "Desktop Entry",
        }
        :param line: {
            "key": "Exec",
            "value": "firefox %u",
            "rawline": "Exec=firefox %u",
        }
        :retruns: true if `fix` can likely fix this line.
        """
        return False

    def fix(self, context, line):
        """Correct the line
        :param context: same as can_fix
        :param line: same as can_fix
        :returns: The fixed (or unchanged) line
        """
        return line["rawline"]


Fixer = _BaseFixer
