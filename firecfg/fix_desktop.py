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

from os import getenv, listdir, mkdir
from os.path import basename, exists, realpath

class Fixer:
    """A fixer can fix one problematic thing in a desktop file"""

    def can_fix(self, context, line):
        """This function is called for every line in the desktop file,
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


class AbsoluteExec(Fixer):
    def can_fix(self, context, line):
        return line["key"] == "Exec" and line["value"][0] == "/"

    def fix(self, context, line):
        command = line["value"].split(" ")
        command[0] = basename(command[0])
        return "Exec=" + " ".join(command)


class DBusActivatable(Fixer):
    def can_fix(self, context, line):
        return line["rawline"] == "DBusActivatable=true"

    def fix(self, context, line):
        return "DBusActivatable=false"


# For tests only
class _RemoveExec(Fixer):
    def can_fix(self, context, line):
        return line["key"] == "Exec"

    def fix(self, context, line):
        return ""


class FixDesktop:
    def __init__(self):
        self._fixers = []
        self._source_dirs = ["/usr/share/applications/", "/usr/local/share/applications/"]
        #self._target_dir = getenv("HOME") + "/.local/share/applications/"
        self._target_dir = "./out/"
        self._symlinks = []

    def load_fixers(self):
        for file in listdir("fixers"):
            if not file.endswith(".py") or file.startswith("_"):
                continue

    def register_fixer(self, fixer):
        self._fixers.append(fixer)

    def _find_program_name(self, file):
        """Return the program name found in the first Exec key in the file."""
        for line in file:
            if line[:5] == "Exec=":
                file.seek(0)
                return basename(line[5:].split(" ", 1)[0].strip())
        return None

    def _has_symlink(self, program_name):
        """Return True if program_name has a symlink in /usr/local/bin pointing to /usr/bin/firejail"""
        if not self._symlinks:
            for entry in listdir("/usr/local/bin"):
                if realpath("/usr/local/bin/" + entry) == "/usr/bin/firejail":
                    self._symlinks.append(entry)
        return program_name in self._symlinks

    def _process_kv_entry(self, ctx, line):
        key, value = line.split("=", 1)
        parsed_line = {
            "key": key,
            "value": value,
            "rawline": line,
        }
        fixed_lines = []
        for fixer in self._fixers:
            if fixer.can_fix(ctx, parsed_line):
                fixed_lines.append(fixer.fix(ctx, parsed_line))
        if len(fixed_lines) == 0:
            out_line = line
        elif len(fixed_lines) == 1:
            out_line = fixed_lines[0]
        else:
            print(f"Multible fixers has suggested a fix for a line in {ctx['program']}.")
            print("0:", line)
            for i in range(1, len(fixed_lines) + 1):
                print(f"{i}: {fixed_lines[i - 1]}")
            choice = int(input("Which one do you want to use? [0,1,...] ").strip())
            if choice == 0:
                out_line = line
            else:
                out_line = fixed_lines[choice - 1]
        return out_line

    def _process_desktop_file(self, sourcedir, file_name):
        cleaned_file = {"data": "#Created by firecfg.py\n", "write": False}
        context = {"filename": file_name, "program": None, "section": None}
        with open(sourcedir + file_name) as ddf:
            context["program"] = self._find_program_name(ddf)
            if not context["program"]:
                print(f"WARN: no Exec key found in '{file_name}'.")
                return
            if not self._has_symlink(context["program"]):
                return
            for line in ddf:
                if line[0] in ("#", "\n"):
                    cleaned_file["data"] += line
                elif line[0] == "[":
                    section = line.strip()[1:-1]
                    cleaned_file["data"] += line
                else:
                    line = line.strip()
                    fixed_line = self._process_kv_entry(context, line)
                    if fixed_line != line:
                        cleaned_file["write"] = True
                    cleaned_file["data"] += fixed_line + "\n"
        if cleaned_file["write"]:
            with open(self._target_dir + file_name, "w") as out_file:
                out_file.write(cleaned_file["data"])


    def fix(self):
        if not exists(self._target_dir):
            mkdir(self._target_dir)
        for source_dir in self._source_dirs:
            for file in listdir(source_dir):
                if file[-8:] == ".desktop":
                    source_dir = "/usr/share/applications/"
                    self._process_desktop_file(source_dir, file)


if __name__ == "__main__":
    FIX_DESKTOP = FixDesktop()
    FIX_DESKTOP.register_fixer(AbsoluteExec())
    FIX_DESKTOP.register_fixer(DBusActivatable())
    #FIX_DESKTOP.register_fixer(_RemoveExec())
    FIX_DESKTOP.fix()
