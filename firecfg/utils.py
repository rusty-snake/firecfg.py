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

"""Various helper functions"""

from os import getenv

def getenv_or(key, default):
    """Return the value of the environment variable key if it exists and it is not empty.
    Otherwise return default."""
    val = getenv(key)
    if not val:
        val = default
    return val

def gen_sources(dirs, subdir):
    """Generate sources for a firejailer.

    :param dirs: A $PATH like string of directories sperated by ':'.
    :param subdir: The name of the directory which is appended to every dir in dirs.
    :returns: A dict with all the sources
    """
    sources = []
    for directory in dirs.split(":"):
        if directory[-1] == "/":
            sources.append(f"{directory}{subdir}/")
        else:
            sources.append(f"{directory}/{subdir}/")
    return sources
