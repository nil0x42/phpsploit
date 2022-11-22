#!/usr/bin/env bash

############################################################
### VALID VALUES
############################################################

valid_schemes="http https socks4 socks4a socks5 socks5h"
invalid_schemes="xxx httpx httpss socks socks4h socks5a"

phpsploit_pipe set PROXY None || FAIL
for scheme in $invalid_schemes; do
    echo invalid_scheme=$scheme
    phpsploit_pipe set PROXY "$scheme://0.0.0.0:23487" > $TMPFILE && FAIL
    assert_contains $TMPFILE "Value Error: Invalid proxy format"
    phpsploit_pipe exploit || FAIL
    phpsploit_pipe exit || FAIL
done

for scheme in $valid_schemes; do
    echo valid_scheme=$scheme
    phpsploit_pipe set PROXY "$scheme://0.0.0.0:23487" > $TMPFILE || FAIL
    assert_no_output $TMPFILE
    phpsploit_pipe set PROXY > $TMPFILE || FAIL
    assert_contains $TMPFILE "$scheme://0.0.0.0:23487"
    phpsploit_pipe exploit > $TMPFILE && FAIL
    if [[ "$scheme" == "socks4"* ]]; then
        assert_contains $TMPFILE "Request error: Error connecting to SOCKS4 proxy "
    elif [[ "$scheme" == "socks5"* ]]; then
        assert_contains $TMPFILE "Request error: Error connecting to SOCKS5 proxy "
    fi
done

# phpsploit_pipe set PROXY https://0.0.0.0:23487 > $TMPFILE || FAIL
# assert_no_output $TMPFILE
# phpsploit_pipe exploit && FAIL

# phpsploit_pipe set PROXY None > $TMPFILE || FAIL
# assert_no_output $TMPFILE
# phpsploit_pipe exploit || FAIL
# phpsploit_pipe exit

# phpsploit_pipe help
