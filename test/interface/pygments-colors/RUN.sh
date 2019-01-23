#!/bin/bash

# check that backdoor php code is colored by pygments on tty
# and not rendered otherwise

cmd="$PHPSPLOIT -s ./commands.phpsploit"

# raw output SHOULD NOT have ansi colors
$cmd > $TMPFILE
grep -Pq '\033\[' $TMPFILE && exit 1

# tty output SHOULD have ansi colors
faketty $cmd > $TMPFILE-2
grep -Pq '\033\[' $TMPFILE-2 || exit 1

# both should be equal after removing ansi colors
sed -ri "s/\x01?\x1B\[(([0-9]+)(;[0-9]+)*)?m\x02?//g" $TMPFILE-2
diff $TMPFILE $TMPFILE-2 || exit 1
