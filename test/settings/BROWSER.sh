#!/usr/bin/env bash

############################################################
### VALID VALUES
############################################################
phpsploit_pipe set BROWSER %%DEFAULT%% > $TMPFILE || FAIL
assert_no_output $TMPFILE

phpsploit_pipe set BROWSER default > $TMPFILE || FAIL
assert_no_output $TMPFILE

# issue #128: BROWSER default fails if no browser available
# Ref: https://github.com/nil0x42/phpsploit/issues/128
phpsploit_pipe set BROWSER disabled > $TMPFILE || FAIL
assert_no_output $TMPFILE

############################################################
### INVALID VALUES
############################################################
phpsploit_pipe set BROWSER invalid_val > $TMPFILE && FAIL
assert_contains $TMPFILE << EOF
^\[\!\] Value Error: Can't bind to 'invalid_val'. Valid choices:
'disabled'
EOF
