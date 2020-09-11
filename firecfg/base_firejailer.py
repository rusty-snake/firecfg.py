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

import logging

from os import listdir, makedirs
from os.path import basename
from re import fullmatch

from . import config
from .fixers import FIXERS

class BaseFirejailer:
    def __init__(self, sources, target, kind, groups):
        self.sources = sources # ["/source/1/", "/source/2/"]
        self.target = target # "/tar/get/"
        self.kind = kind # "applications"
        self.fixers = [fixer for fixer in FIXERS if fixer.KIND.endswith(self.kind)]
        self.programs = groups.programs[self.kind]

    def _find_program_name(self, file):
        """Return the program name found in the first Exec key in the file."""
        for line in file:
            if line[:5] == "Exec=":
                file.seek(0)
                return basename(line[5:].split(" ", 1)[0].strip())
        return None

    def _firejailing_enabled_for(self, data):
        for line in data:
            if line.startswith("Exec="):
                line_splited = line[5:].split(" ")
                prg = basename(line_splited[0].strip())
                if prg == "firejail":
                    prg = basename(line_splited[1].strip())
                return prg in self.programs
        return None

    def _get_fixers(self, ctx):
        """Return a list with all fixer that should be applied for ctx"""
        fixers = []
        for fixer in self.fixers:
            if fixer.KIND[:7] == "general":
                fixers.append(fixer)
            elif fixer.KIND[:7] == "special":
                for regex in fixer.FILES:
                    if fullmatch(regex, ctx["source_file_name"]):
                        fixers.append(fixer)
            else:
                raise ValueError
        return fixers

    def _process_kvline(self, kvline, ctx):
        fixed_lines = []
        for fixer in self._get_fixers(ctx):
            if fixer.can_fix(ctx, kvline):
                fixed_lines.append(fixer.fix(ctx, kvline))
        if len(fixed_lines) == 0:
            out_line = kvline["rawline"]
        elif len(fixed_lines) == 1:
            out_line = fixed_lines[0]
        else:
            print(fixed_lines)
            print(f"Multible fixers has suggested a fix for a line in {ctx['program_name']}.")
            print("0:", kvline["rawline"])
            for i in range(1, len(fixed_lines) + 1):
                print(f"{i}: {fixed_lines[i - 1]}")
            choice = int(input("Which one do you want to use? [0,1,...] ").strip())
            if choice == 0:
                out_line = kvline["rawline"]
            else:
                out_line = fixed_lines[choice - 1]
        return out_line

    def _firejail_source_file(self, source_file, ctx):
        fixed_file = []
        write_file = False
        for line in source_file:
            line = line.strip()
            if line == "":
                fixed_file.append("")
            elif line[0] == "#":
                fixed_file.append(line)
            elif line[0] == "[":
                ctx["section"] = line[1:-1]
                fixed_file.append(line)
            else:
                key, value = line.split("=", 1)
                kvline = {
                    "key": key,
                    "value": value,
                    "rawline": line,
                }
                out_line = self._process_kvline(kvline, ctx)
                fixed_file.append(out_line)
                if out_line != line:
                    write_file = True
        if write_file and self._firejailing_enabled_for(fixed_file):
            if fixed_file[-1] != "\n":
                fixed_file.append("")
            logging.info(f"Fixing {ctx['source_file_name']}")
            with open(ctx["target_file_path"], "w") as target_file:
                target_file.write("\n".join(fixed_file))

    def _firejail_nth_source(self, n):
        try:
            for file_name in listdir(self.sources[n]):
                if not isfile(self.sources[n] + file_name):
                    continue
                try:
                    with open(self.sources[n] + file_name) as source_file:
                        ctx = {
                            "source_dir": self.sources[n],
                            "source_file_name": file_name,
                            "source_file_path": self.sources[n] + file_name,
                            "target_file_path": self.target + file_name,
                            "program_name": self._find_program_name(source_file),
                            "section": None,
                        }
                        self._firejail_source_file(source_file, ctx)
                except Exception as err:
                    logging.warning(f"An error ocured while processing '{file_name}' in '{self.sources[n]}': {err}")
                    if config.DEBUG:
                        raise
        except FileNotFoundError:
            pass
        if n + 1 < len(self.sources):
            self._firejail_nth_source(n + 1)

    def before(self):
        pass

    def after(self):
        pass

    def firejail(self):
        self.before()
        makedirs(self.target, mode=0o0755, exist_ok=True)
        self._firejail_nth_source(0)
        self.after()
