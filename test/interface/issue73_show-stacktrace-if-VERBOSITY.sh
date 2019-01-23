#!/bin/bash

# Issue #73: Show stack trace when VERBOSITY is True
# ref: https://github.com/nil0x42/phpsploit/issues/73

stacktrace='Traceback (most recent call last)'

# this SHOULD NOT contain stack trace:
$PHPSPLOIT -e 'set VERBOSITY False; source /; true' > $TMPFILE
grep -q "$stacktrace" $TMPFILE && exit 1

# this SOULD contain stack trace:
$PHPSPLOIT -e 'set VERBOSITY True; source /; true' > $TMPFILE
grep -q "$stacktrace" $TMPFILE || exit 1
