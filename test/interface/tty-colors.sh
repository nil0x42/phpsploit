#!/bin/bash

# check that tty colors are rendered within a tty
# and not rendered otherwise

cat > $TMPFILE-src << EOF
# phpsploit source file
help help
INV4LID_COMMAND
source /INV4LID_PATH
set BACKDOOR "@eval(\$_SERVER['HTTP_%%PASSKEY%%'])"
set BACKDOOR
set REQ_INTERVAL 1-10
set REQ_INTERVAL
set VERBOSITY "TRUE"
set VERBOSITY "FALSE"
exploit --get-backdoor
EOF

cmd="$PHPSPLOIT -s $TMPFILE-src"

# raw output SHOULD NOT have ansi colors
$cmd > $TMPFILE || FAIL
grep -Pq '\033\[' $TMPFILE && FAIL

# tty output SHOULD have ansi colors
faketty $cmd > $TMPFILE-2
grep -Pq '\033\[' $TMPFILE-2 || FAIL

# assert file contains at least 500 ansi colors
ansi_colors=$(perl -lne 'END {print $c} $c += s/\033\[//g' $TMPFILE-2)
[ "$ansi_colors" -lt 500 ] && FAIL $ansi_colors

# ensure `exploit --get-backdoor` gets colored by pygments
ansi_colors=$(grep -v BACKDOOR $TMPFILE-2 | grep HTTP_PHPSPL01T \
    | perl -lne 'END {print $c} $c += s/\033\[//g')
[ "$ansi_colors" -lt 9 ] && FAIL $ansi_colors

# both should be equal after removing ansi colors
decolorize $TMPFILE-2
diff $TMPFILE $TMPFILE-2 || FAIL
