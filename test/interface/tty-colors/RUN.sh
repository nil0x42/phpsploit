#!/bin/bash

# check color rendering of output wrapper

function faketty () {
    script -eqc "$1" /dev/null
}

cmd="$PHPSPLOIT -s ./commands.phpsploit"

# check raw output integrity
$cmd > "$TMPFILE"
diff --color=auto ./expected-raw-output.txt "$TMPFILE"

# check tty colored output integrity
faketty "$cmd" > "$TMPFILE"
diff --color=auto ./expected-tty-output.txt "$TMPFILE"
