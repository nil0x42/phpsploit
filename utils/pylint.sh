#!/bin/bash

SCRIPTDIR="$(readlink -f `dirname $0`)"
BASEDIR="$(git -C \"$SCRIPTDIR\" rev-parse --show-toplevel)"

# add ./src & ./deps/*/ to PYTHONPATH
src="$BASEDIR/src"
deps=$(find "$BASEDIR/deps" -mindepth 1 -maxdepth 1 '!' -name '__*' | paste -sd:)
PYTHONPATH=":${src}:${deps}:${PYTHONPATH}"

pre_args="--good-names=e,x,i,p,m --disable=no-member,not-callable"
if [ -z "$1" ]; then
    args="$BASEDIR/phpsploit $BASEDIR/src/"
    exec pylint3 $pre_args $args
else
    exec pylint3 $pre_args "$@"
fi
