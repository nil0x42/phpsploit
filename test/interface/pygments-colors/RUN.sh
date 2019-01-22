#!/bin/bash

# check that backdoor php code is colored by pygments on tty
# and not rendered otherwise

cmd="$PHPSPLOIT -s ./commands.phpsploit"

###
### check raw/colorless output
###
$cmd | tee $TMPFILE
# assert NO ANSI colors present
! grep -Pq '\033\[' $TMPFILE

###
### check tty/colored output
###
faketty $cmd | tee $TMPFILE-2
# assert ANSI colors present
grep -Pq '\033\[' $TMPFILE-2

# remove ANSI colors from file2, and check it's the same as file1
sed -ri "s/\x01?\x1B\[(([0-9]+)(;[0-9]+)*)?m\x02?//g" $TMPFILE-2
diff $TMPFILE $TMPFILE-2
