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

from os import symlink
from os.path import islink, realpath
from re import compile as compile_re
from shutil import which

class CreateSymlinks:
    ALLOWED_PATTERN = compile_re("[a-zA-Z0-9_.-]+")
    FIREJAIL_EXEC = "/usr/bin/firejail"
    BINDIR = "/usr/local/bin/"

    def __init__(self):
        self.groups = ["firecfg.config-dummy"]

    def _is_restricted(self, name):
        return not (name == ".." or not CreateSymlinks.ALLOWED_PATTERN.fullmatch(name))

    def _process_group(self, group):
        for line in group:
            if line[0] == "#":
                continue
            prg = line.strip()
            if self._is_restricted(prg) is False:
                print(f"WARN: Skipping program '{prg}' because it contains disallowed characters")
                continue
            if which(prg):
                try:
                    print(f"Create symlink for {prg}")
                    symlink(CreateSymlinks.FIREJAIL_EXEC, CreateSymlinks.BINDIR + prg)
                except FileExistsError:
                    if islink(CreateSymlinks.BINDIR + prg) \
                      and realpath(CreateSymlinks.BINDIR + prg) == CreateSymlinks.FIREJAIL_EXEC:
                        print(CreateSymlinks.BINDIR + prg)
                        print(f"INFO: Symlink for '{prg}' already exists")
                    else:
                        print(f"WARN: Can not create symlink for '{prg}': FileExistsError")
            else:
                #print(f"Create no symlink for {prg}")
                pass


    def create(self):
        if not self.groups:
            raise Exception("groups must contain at least one group")

        for group in self.groups:
            if self._is_restricted(group) is False:
                print(f"WARN: Skipping group '{group}' because it contains disallowed characters")
                continue
            #with open("/etc/firecfg.py/groups/" + group) as group_fd:
            with open("/usr/lib64/firejail/firecfg.config") as group_fd:
                self._process_group(group_fd)

if __name__ == "__main__":
    CreateSymlinks().create()
