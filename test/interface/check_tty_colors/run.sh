#!/bin/bash

# check color rendering of output wrapper

SCRIPTDIR="$(realpath `dirname $0`)"
BASEDIR="$(git rev-parse --show-toplevel)"
cd "$BASEDIR"

function faketty () {
    script -eqc "$1" /dev/null
}

set -ve

cmd="./phpsploit -c 'data/config/config' -s '$SCRIPTDIR/commands.phpsploit'"
tmpfile=`mktemp`

# check raw output integrity
$cmd > "$tmpfile"
cat "$tmpfile"
echo diff --color=auto "$tmpfile" "$SCRIPTDIR/expected-raw-output.txt"
diff --color=auto "$tmpfile" "$SCRIPTDIR/expected-raw-output.txt"

# check tty colored output integrity
faketty "$cmd" > "$tmpfile"
cat "$tmpfile"
echo diff --color=auto "$tmpfile" "$SCRIPTDIR/expected-tty-output.txt"
diff --color=auto "$tmpfile" "$SCRIPTDIR/expected-tty-output.txt"



# colored_output=`faketty "$cmd"`
# echo "$colored_output"
# colored_output_md5=`echo "$colored_output" | md5sum | cut -d' ' -f1`
# echo "$colored_output_md5"
# [ "$colored_output_md5" == "8ab9ff0d849195ecbcb6ca2a1834eab0" ]
