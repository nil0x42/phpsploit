#!/bin/bash

###
### func tests for phpsploit launcher (./phpsploit)
###

###
### Early Ctrl-C interrupt (SIGINT)
###
timeout -s INT 0.05 $RAW_PHPSPLOIT --help > $TMPFILE-out 2> $TMPFILE
assert_contains $TMPFILE "\[-\] .* initialization interrupted$"
rm $TMPFILE-out

###
### Check Random Message presence in interactive/TTY mode
###
faketty $PHPSPLOIT -ie exit > $TMPFILE
decolorize $TMPFILE
common=$(comm -12 <(sort $TMPFILE) <(sort $ROOTDIR/data/messages.lst) | wc -l)
[ "$common" -eq 1 ] || FAIL

###
### Use phpsploit as a script's shebang
###
cat > $TMPFILE-script << EOF
#!$RAW_PHPSPLOIT
session
EOF
chmod +x $TMPFILE-script
$TMPFILE-script > $TMPFILE
grep -qi '^phpsploit session' $TMPFILE || FAIL
# test with $PHPSPLOIT (to make coverage happy)
$PHPSPLOIT $TMPFILE-script > $TMPFILE
grep -qi '^phpsploit session' $TMPFILE || FAIL
rm $TMPFILE-script
