#!/usr/bin/python3

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

from os import listdir

def listdir_sorted(path):
    files = listdir(path)
    files.sort()
    return files

firecfg_config = []
with open("/usr/lib64/firejail/firecfg.config") as raw_firecfg_config:
    for line in raw_firecfg_config:
        if line[0] == "#":
            continue
        firecfg_config.append(line.strip())

out = """\
# This file is automatically generated by gen_groups.py,
# based on firecfg.config and /etc/firejail/*.profile.
#
# The format is the following:
# The format is as follows:
# <program-name/firejail-profile-name>=<places to firejail>
# Where <places to firejail> is a comma separated list consisting of
# - applications: $XDG_DATA_DIRS/applications
# - autostart: $XDG_CONFIG_DIRS/autostart
# - dbus-service: $XDG_DATA_DIRS/dbus-1/services
# - symlink: $PATH
# You can also mark a places as explicitly unset by prefixing it with a '!'.
# You can also mark places as explicitly unset by prefixing it with a '!'.
#
# Groups are first read from the system-locations and the from the user-location.
# Groups are first read from the system-locations and then from the user-location.
# Inside a location the groups are read alphabetically (numbers, upper, lower).
#
# By confection groups shipped by firecfg.py start with a uppercase letter (and this file with a 0).
# User customization should go in a file starting with a lowercase letter.
# By design groups shipped by firecfg.py start with an uppercase letter (and this file with a 0).
# User customizations should go in a file starting with a lowercase letter.
"""
for filename in listdir_sorted("/etc/firejail"):
    if not filename.endswith(".profile") or filename.endswith("common.profile"):
        continue
    prg = filename[:-8]
    if prg in ("default", "server"):
        continue
    if prg in firecfg_config:
        out += prg + "=applications,symlink\n"
    else:
        out += prg + "=\n"

with open("generated_groups.txt", "w") as out_file:
    out_file.write(out)
