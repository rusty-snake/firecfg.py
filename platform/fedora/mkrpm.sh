#!/bin/bash

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

set -e

usage() {
	cat <<EOM
USAGE

    $0 [--help|--use-mock]

        --help  Show this help and exit.
        --use-mock  Build the rpm using mock.
          This requires that mock is installed and the user is allowed to use it.
EOM
}

if [ "$1" == "--help" ]; then
	usage
	exit 0
fi

if ! command -v rpmbuild >/dev/null; then
	echo "Please install rpmbuild: sudo dnf install rpm-build"
	exit 1
fi

TOPDIR=$(mktemp -dt firecfg.py-build.XXXXXX)
SOURCEDIR=$(rpm --define "_topdir $TOPDIR" --eval %_sourcedir)
SPECDIR=$(rpm --define "_topdir $TOPDIR" --eval %_specdir)
BUILDDIR=$(rpm --define "_topdir $TOPDIR" --eval %_builddir)
RPMDIR=$(rpm --define "_topdir $TOPDIR" --eval %_rpmdir)
SRPMDIR=$(rpm --define "_topdir $TOPDIR" --eval %_srcrpmdir)

mkdir -p "$BUILDDIR" "$RPMDIR" "$SOURCEDIR" "$SPECDIR" "$SRPMDIR"
# shellcheck disable=SC2064
trap "rm -rf '$TOPDIR'" EXIT

cp "$(dirname "$0")"/firecfg.py.spec "$SPECDIR"
REPO_ROOT="$(while [[ ! -d .git && $PWD != / ]]; do cd ..; done && [[ $PWD != / ]] && echo "$PWD")"
tar --transform "s|${REPO_ROOT#/}|.|" --exclude=".git" -czf "$SOURCEDIR/firecfg.py.tar.gz" "$REPO_ROOT"

if [ "$1" == "--use-mock" ]; then
	rpmbuild --define "_topdir $TOPDIR" -bs "$SPECDIR"/firecfg.py.spec

	mock "$SRPMDIR"/*.rpm
else
	rpmbuild --define "_topdir $TOPDIR" -ba "$SPECDIR"/firecfg.py.spec

	cp "$RPMDIR"/*/*.rpm "$SRPMDIR"/*.rpm .
fi
