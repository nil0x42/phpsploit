#!/bin/bash

###
### func tests for phpsploit launcher (./phpsploit)
###

###
### Early Ctrl-C interrupt (SIGINT)
###
> $TMPFILE
# testing different timeouts because it depends on time needed
# to load phpsploit for current platform/interpreter
timeout -s INT 0.05 $RAW_PHPSPLOIT --help > $TMPFILE-out 2>> $TMPFILE
timeout -s INT 0.1 $RAW_PHPSPLOIT --help > $TMPFILE-out 2>> $TMPFILE
timeout -s INT 0.15 $RAW_PHPSPLOIT --help > $TMPFILE-out 2>> $TMPFILE
timeout -s INT 0.2 $RAW_PHPSPLOIT --help > $TMPFILE-out 2>> $TMPFILE
assert_contains $TMPFILE "\[-\] .* initialization interrupted$"
rm $TMPFILE-out

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
