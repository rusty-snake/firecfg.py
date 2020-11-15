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

from . import config
from .base_firejailer import BaseFirejailer
from .utils import getenv_or, gen_sources

class ApplicationsFirejailer(BaseFirejailer):
    def __init__(self, groups):
        sources = gen_sources(getenv_or("XDG_DATA_DIRS", "/usr/local/share:/usr/share"),
                              "applications")
        target = config.prefix + "overrides/share/applications/"
        super().__init__(sources, target, kind="applications", groups=groups)
