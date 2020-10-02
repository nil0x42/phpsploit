#!/bin/bash

SCRIPTDIR="$(readlink -f `dirname $0`)"
BASEDIR="$(git -C "$SCRIPTDIR" rev-parse --show-toplevel)"

# add ./src to PYTHONPATH
src="$BASEDIR/src"
PYTHONPATH=":${src}:${PYTHONPATH}"

pre_args="--good-names=e,x,i,p,m --disable=no-member,not-callable"
if [ -z "$1" ]; then
    # default args (if not defined in argv[1:])
    args="$BASEDIR/phpsploit $BASEDIR/src/"
    exec /usr/bin/pylint3 $pre_args $args
else
    exec /usr/bin/pylint3 $pre_args "$@"
fi
