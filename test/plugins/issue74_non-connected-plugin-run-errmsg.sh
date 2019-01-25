#!/bin/bash

# Issue #74:
# Make warning message explicit when running plugin in non-connected mode
# ref: https://github.com/nil0x42/phpsploit/issues/74

phpsploit_pipe 'pwd' > $TMPFILE && FAIL
grep -q 'Must connect to run `pwd` plugin' $TMPFILE || FAIL

$PHPSPLOIT -e 'exploit; pwd' > $TMPFILE || FAIL
grep -q 'Must connect to run `pwd` plugin' $TMPFILE && FAIL
