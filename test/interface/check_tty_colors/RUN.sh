#!/bin/bash

# check color rendering of output wrapper

SCRIPTDIR="$(realpath `dirname $0`)"
BASEDIR="$(git rev-parse --show-toplevel)"
cd "$BASEDIR"

function faketty () {
    script -eqc "$1" /dev/null
}


cmd="./phpsploit -c 'data/config/config' -s '$SCRIPTDIR/commands.phpsploit'"
tmpfile=`mktemp`

echo PWD=$PWD
echo cmd=$cmd
echo tmpfile=$tmpfile

set -ve

# check raw output integrity
$cmd > "$tmpfile"
diff --color=auto "$SCRIPTDIR/expected-raw-output.txt" "$tmpfile"

# check tty colored output integrity
faketty "$cmd" > "$tmpfile"
diff --color=auto "$SCRIPTDIR/expected-tty-output.txt" "$tmpfile"

rm "$tmpfile"
