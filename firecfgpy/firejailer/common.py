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

"""Classes for firejailers with shared code"""

import logging
from os import getenv, listdir, makedirs
from os.path import basename
from os.path import join as join_paths

from . import FIREJAIL, FireJailer


class PrependFirejailInExecKeys(FireJailer):
    """Base class for firejailers parsing a ini-like file with ``Exec=<command-line>``"""

    SOURCES_ENV: str = NotImplemented
    SOURCES_DEFAULT: str = NotImplemented
    SOURCES_SUBDIR: str = NotImplemented
    TARGET_SUFFIX: str = NotImplemented

    @classmethod
    def run(cls, programs: set[str], overrides: str) -> None:
        targetdir = join_paths(overrides, cls.TARGET_SUFFIX)
        makedirs(targetdir, mode=0o0755, exist_ok=True)

        srcdirprefixes = getenv(cls.SOURCES_ENV) or cls.SOURCES_DEFAULT
        for srcdirprefix in srcdirprefixes.split(":"):
            srcdir = join_paths(srcdirprefix, cls.SOURCES_SUBDIR)
            try:
                for filename in listdir(srcdir):
                    firejailed = False
                    newfile: list[str] = []
                    try:
                        with open(join_paths(srcdir, filename)) as file:
                            for line in file:
                                if line.startswith("Exec="):
                                    cmdl = line[5:].rstrip().split(" ")
                                    if "/" not in cmdl[0]:
                                        newfile += line
                                    elif basename(cmdl[0]) in programs:
                                        newfile += f"Exec={FIREJAIL} {' '.join(cmdl)}\n"
                                        firejailed = True
                                    else:
                                        newfile += line
                                else:
                                    newfile += line
                    except:
                        raise
                    if firejailed is True:
                        try:
                            logging.debug("Firejail %s %s", cls.NAME, filename)
                            with open(join_paths(targetdir, filename), "w") as file:
                                file.write("".join(newfile))
                        except:
                            raise
            except FileNotFoundError as err:
                if err.filename != srcdir:
                    raise
