#!/bin/bash

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

# '${!foo}' is a bashism and does not work in e.g. ksh or zsh.
[ -n "$BASH_VERSION" ] || return 0

__FCP_SYSTEM_OVERRIDES_PREFIX="/etc/firecfg.py/overrides"
__FCP_USER_OVERRIDES_PREFIX="$HOME/.config/firecfg.py/overrides"

# Prepend $2 to the variable with name $1, if $1 does not already
# contain $2. $3 is a fallback value for $1.
__fcp_prepend_env() {
	[[ ":${!1}:" == *":$2:"* ]] || declare -g "$1=$2:${!1:-$3}"
}

# add system-wide overrides
__fcp_prepend_env PATH "$__FCP_SYSTEM_OVERRIDES_PREFIX/bin" /usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
__fcp_prepend_env XDG_DATA_DIRS "$__FCP_SYSTEM_OVERRIDES_PREFIX/share" /usr/local/share:/usr/share
__fcp_prepend_env XDG_CONFIG_DIRS "$__FCP_SYSTEM_OVERRIDES_PREFIX/xdg" /etc/xdg

# add user overrides for all regular users
if [[ ${UID:-$(id -u)} -ge 1000 ]]; then
	__fcp_prepend_env PATH "$__FCP_USER_OVERRIDES_PREFIX/bin"
	__fcp_prepend_env XDG_DATA_DIRS "$__FCP_USER_OVERRIDES_PREFIX/share"
	__fcp_prepend_env XDG_CONFIG_DIRS "$__FCP_USER_OVERRIDES_PREFIX/xdg"
fi

unset __fcp_prepend_env __FCP_SYSTEM_OVERRIDES_PREFIX __FCP_USER_OVERRIDES_PREFIX

if (return 0 2>/dev/null); then
	# sourced from /etc/profile.d
	export PATH
	export XDG_DATA_DIRS
	export XDG_CONFIG_DIRS
else
	# executed as systemd.environment-generator
	echo "PATH=$PATH"
	echo "XDG_DATA_DIRS=$XDG_DATA_DIRS"
	echo "XDG_CONFIG_DIRS=$XDG_CONFIG_DIRS"
fi
