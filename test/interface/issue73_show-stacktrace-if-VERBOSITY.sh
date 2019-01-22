#!/bin/bash

# Show stack trace when VERBOSITY is True
#
# Issue: #73
# Ref: https://github.com/nil0x42/phpsploit/issues/73

stacktrace='Traceback (most recent call last):'

# this SHOULD NOT contain stack trace:
$PHPSPLOIT -e 'set VERBOSITY False; source /; lrun true' > $TMPFILE
! grep "$stacktrace" $TMPFILE

# this SOULD contain stack trace:
$PHPSPLOIT -e 'set VERBOSITY True; source /; lrun true' > $TMPFILE
grep -q "$stacktrace" $TMPFILE
