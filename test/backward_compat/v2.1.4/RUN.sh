#!/bin/bash

< $SCRIPTDIR/phpsploit.session \
    sed -e "s/127.0.0.1:64956/$TARGET/g" \
    > $TMPDIR/tmp-session

$PHPSPLOIT -e "session load $TMPDIR/tmp-session" || FAIL

phpsploit_pipe session load $TMPDIR/tmp-session || FAIL

# this one must FAIL (not confirming env reset)
phpsploit_pipe "exploit\nN" > $TMPFILE && FAIL
assert_contains $TMPFILE "TARGET server have changed, are you sure you want to reset environment as shown above"
assert_contains $TMPFILE "Exploitation aborted"

# this one must SUCCEED (confirming env reset)
phpsploit_pipe "exploit\nY" > $TMPFILE || FAIL
assert_contains $TMPFILE "TARGET server have changed, are you sure you want to reset environment as shown above"
assert_contains $TMPFILE "Environment correctly reset"
assert_contains $TMPFILE "Shell obtained by PHP"
