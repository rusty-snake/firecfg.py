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

# '${!foo}' is a bash thing that does not work in ksh, zsh.
[ -n "$BASH_VERSION" ] || return 0

SYSTEM_PREFIX="/etc/firecfg.py/overrides"
USER_PREFIX="$HOME/.config/firecfg.py/overrides"

# return 0 if $1 contains $2, otherwise return 1
contains() {
	local OLDIFS="$IFS"
	IFS=":"
	for path in $1; do
		if [[ "$path" == "$2" ]]; then
			IFS="$OLDIFS"
			return 0
		fi
	done
	IFS="$OLDIFS"
	return 1
}

# Prepend $2 to the variable with name $1, if $1 does not already
# contain $1. $3 is a fallback value for $1.
prepend_env() {
	if contains "${!1}" "$2"; then
		return 0
	fi
	# shellcheck disable=SC2140
	declare -g "$1"="$2:${!1:-$3}"
}

# add system-wide overrides
prepend_env PATH "$SYSTEM_PREFIX/bin" /usr/local/bin:/usr/local/sbin:/usr/bin:/usr/sbin
prepend_env XDG_DATA_DIRS "$SYSTEM_PREFIX/share" /usr/local/share:/usr/share
prepend_env XDG_CONFIG_DIRS "$SYSTEM_PREFIX/xdg" /etc/xdg

# add user overrides for all regular users
if [ $UID -ge 1000 ]; then
	prepend_env PATH "$USER_PREFIX/bin"
	prepend_env XDG_DATA_DIRS "$USER_PREFIX/share"
	prepend_env XDG_CONFIG_DIRS "$USER_PREFIX/xdg"
fi

unset contains prepend_env SYSTEM_PREFIX USER_PREFIX

if (return 0 2>/dev/null); then
	# sourced from /etc/profile.d
	export PATH
	export XDG_DATA_DIRS
	export XDG_CONFIG_DIRS
else
	# executed from /usr/lib/systemd/{system,user}-environment-generators
	echo "PATH=$PATH"
	echo "XDG_DATA_DIRS=$XDG_DATA_DIRS"
	echo "XDG_CONFIG_DIRS=$XDG_CONFIG_DIRS"
fi
