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

"""firecfg.py"""

import argparse
import logging
from os import getenv, getuid
from os.path import expanduser
from shutil import rmtree

from firecfgpy.firejail_users import FirejailUsers
from firecfgpy.firejailer.firejailers import FIREJAILERS
from firecfgpy.groups import Groups
from firecfgpy.setup_firecfgpy import setup_firecfgpy


def main() -> None:
    """main-function, entry point from the command-line"""

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    parser_setup = subparsers.add_parser("setup")
    args = parser.parse_args()

    logging.basicConfig(
        format="%(levelname)s(firecfg.py): %(message)s",
        level=logging.DEBUG,
    )

    if args.subcommand == "setup":
        setup_firecfgpy()
        return

    if getuid() == 0:
        overrides = "/etc/firecfg.py/overrides"
    else:
        overrides = expanduser("~/.config/firecfg.py/overrides")

    try:
        logging.info("Delete old overrides at %s", overrides)
        rmtree(overrides)
    except FileNotFoundError as err:
        if err.filename != overrides:
            raise

    groups = Groups()
    groups.load_all()

    for firejailer in FIREJAILERS:
        firejailer.run(groups[firejailer.ID], overrides)

    if getuid() == 0:
        if sudo_user := getenv("SUDO_USER"):
            firejail_users_db = FirejailUsers()
            try:
                firejail_users_db.read()
            except FileNotFoundError:
                pass
            firejail_users_db.add(sudo_user)
            firejail_users_db.write()


if __name__ == "__main__":
    main()
