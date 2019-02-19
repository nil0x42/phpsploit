#!/bin/bash

# Issue #73: Show stack trace when VERBOSITY is True
# ref: https://github.com/nil0x42/phpsploit/issues/73

stacktrace='Traceback (most recent call last)'

# this SHOULD NOT contain stack trace:
$PHPSPLOIT -e 'set VERBOSITY False; source /' > $TMPFILE && FAIL
grep -q "$stacktrace" $TMPFILE && FAIL

# this SOULD contain stack trace:
$PHPSPLOIT -e 'set VERBOSITY True; source /' > $TMPFILE && FAIL
grep -q "$stacktrace" $TMPFILE || FAIL
