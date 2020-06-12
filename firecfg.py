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

from os import getenv, getuid, setgid, setgroups, setuid
from sys import exit as sys_exit

from firecfg.clean_symlinks import CleanSymlinks
from firecfg.create_symlinks import CreateSymlinks
from firecfg.fix_desktop import FixDesktop

def main():
    if getuid() != 0:
        print("ERROR: Need to be root")
        sys_exit(1)

    CleanSymlinks().clean()
    CreateSymlinks().create()

    uid = int(getenv("SUDO_UID"))
    gid = int(getenv("SUDO_GID"))
    if uid and gid:
        setgroups([])
        setgid(gid)
        setuid(uid)

        fix_desktop = FixDesktop()
        fix_desktop.load_fixers()
        fix_desktop.fix()

if __name__ == "__main__":
    main()
