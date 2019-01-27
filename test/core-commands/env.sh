#!/usr/bin/env bash

############################################################
### NON-CONNECTED MODE
############################################################

# issue #53: env: Confusing error message before `exploited` context
# Ref: https://github.com/nil0x42/phpsploit/issues/53
phpsploit_pipe env > $TMPFILE && FAIL
grep -q '^\[\-\] Must connect to spread env vars ' $TMPFILE || FAIL
phpsploit_pipe env PWD > $TMPFILE && FAIL
grep -q '^\[\-\] Must connect to spread env vars ' $TMPFILE || FAIL
