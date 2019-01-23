#!/usr/bin/env bash

# issue #70: get help for `CMD` when calling `help CMD ARG`
# Ref: https://github.com/nil0x42/phpsploit/issues/70
# ensure this gives help for `corectl`:
$PHPSPLOIT -e 'help corectl FOOBAR' > $TMPFILE
grep -q '^\[\*\] corectl: ' $TMPFILE || exit 1


