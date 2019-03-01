#!/bin/bash

# test behavior of `corectl display-http-requests`

# should fail with msg if no requests were sent:
phpsploit_pipe corectl display-http-requests > $TMPFILE && FAIL
assert_contains $TMPFILE << EOF
^\[-\] From now, phpsploit didn't sent any HTTP(s) request$
EOF


# after exploit, a single GET request is present:
phpsploit_pipe exploit > $TMPFILE || FAIL
phpsploit_pipe corectl display-http-requests > $TMPFILE || FAIL
assert_contains $TMPFILE << EOF
^\[\*\] Listing last payload's HTTP(s) requests:$
^### REQUEST 1$
^GET / HTTP/1.1$
^Accept-Encoding: identity$
^Connection: close$
^Zzaa: 
^Zzab: 
EOF
assert_not_contains $TMPFILE << EOF
^\[-\] From now, phpsploit didn't sent any HTTP(s) request$
^### REQUEST 2$
^POST / HTTP/1.1$
^phpSpl01t=
EOF
[ "$(grep -c REQUEST $TMPFILE)" -eq 1 ] || FAIL


# use POST method, with 2k POST_DATA limitation, and check that all
# requests were logged as expected after running `ls` plugin:
phpsploit_pipe set REQ_DEFAULT_METHOD POST > $TMPFILE || FAIL
phpsploit_pipe set REQ_MAX_POST_SIZE 2k > $TMPFILE || FAIL

phpsploit_pipe "ls\nP" > $TMPFILE-x # add P to confirm multireq by POST
num_reqs=$(grep 'will be' $TMPFILE-x | sed -E 's/.* ([0-9]+) .* will be .*/\1/')

phpsploit_pipe corectl display-http-requests > $TMPFILE || FAIL
[ "$(grep -c REQUEST $TMPFILE)" -eq "$num_reqs" ] || FAIL $num_reqs
assert_contains $TMPFILE << EOF
^\[\*\] Listing last payload's HTTP(s) requests:$
^### REQUEST 1$
^### REQUEST 2$
^### REQUEST $num_reqs$
^POST / HTTP/1.1$
^phpSpl01t=
EOF
assert_not_contains $TMPFILE << EOF
^\[-\] From now, phpsploit didn't sent any HTTP(s) request$
^### REQUEST $(( $num_reqs + 1 ))$
^GET / HTTP/1.1$
^Zzaa: 
^Zzab: 
EOF
