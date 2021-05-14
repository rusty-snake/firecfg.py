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

"""Post-install setup"""

from os import chmod, listdir, makedirs
from pathlib import Path
from shutil import copyfile


def setup_firecfgpy() -> None:
    """Post-install setup function

    This functions add ``zz-firecfg.py.sh`` to
      - ``/etc/profile.d``
      - ``/etc/systemd/system-environment-generators``
      - ``/etc/systemd/user-environment-generators``

    and installs additional firejail profiles.
    """

    makedirs("/etc/firejail", mode=0o0755, exist_ok=True)
    makedirs("/etc/profile.d", mode=0o0755, exist_ok=True)
    makedirs("/etc/systemd/system-environment-generators", mode=0o0755, exist_ok=True)
    makedirs("/etc/systemd/user-environment-generators", mode=0o0755, exist_ok=True)

    setup_data_dir = Path(__file__).parent / "setup_data"

    copyfile(setup_data_dir / "zz-firecfg.py.sh", "/etc/profile.d/zz-firecfg.py.sh")
    copyfile(
        setup_data_dir / "zz-firecfg.py.sh",
        "/etc/systemd/system-environment-generators/zz-firecfg.py.sh",
    )
    chmod("/etc/systemd/system-environment-generators/zz-firecfg.py.sh", 0o0755)
    copyfile(
        setup_data_dir / "zz-firecfg.py.sh",
        "/etc/systemd/user-environment-generators/zz-firecfg.py.sh",
    )
    chmod("/etc/systemd/user-environment-generators/zz-firecfg.py.sh", 0o0755)

    for filename in listdir(setup_data_dir / "firejail"):
        copyfile(
            setup_data_dir / "firejail" / filename, Path("/etc/firejail") / filename
        )
