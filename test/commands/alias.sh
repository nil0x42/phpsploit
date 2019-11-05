#!/usr/bin/env bash

###
### CHECK ALIAS WARNINGS
### XXX: PUTTING THIS ON TOP OF TEST FILE BECAUSE SHOULD WORK EVEN IF NOT CONNECTED
###

# deleting an existing alias:
# issue #59: `alias <VAR> None` misses verbosity
phpsploit_pipe alias FOO BAR > $TMPFILE || FAIL
[[ $(count_lines $TMPFILE) -eq 0 ]] || FAIL
phpsploit_pipe alias FOO None > $TMPFILE || FAIL
assert_contains $TMPFILE 'alias correctly deleted'

# overriding an existing alias:
phpsploit_pipe alias FOO BAR > $TMPFILE || FAIL
[[ $(count_lines $TMPFILE) -eq 0 ]] || FAIL
phpsploit_pipe alias FOO None > $TMPFILE || FAIL
assert_contains $TMPFILE 'alias correctly deleted'

# overriding an existing core command:
phpsploit_pipe alias history BAR > $TMPFILE || FAIL
assert_contains $TMPFILE ' command overridden'

# overriding an existing plugin:
phpsploit_pipe alias stat BAR > $TMPFILE || FAIL
assert_contains $TMPFILE ' plugin overridden'



###
### CHECK ALIAS CREATION & NESTING BEHAVIOR
###

# create misc aliases for test
phpsploit_pipe alias l-startsiwhL FOO > $TMPFILE || FAIL
phpsploit_pipe alias l-startsiwhLagain BAR > $TMPFILE || FAIL
phpsploit_pipe alias idontstartWithL BAZ > $TMPFILE || FAIL

# this should only show aliases starting with 'l'
phpsploit_pipe alias l > $TMPFILE
sed -e '1,/---/d' -e '/^$/,$d' $TMPFILE | grep -vq '^    l' && FAIL

# but calling `alias` alone lists all aliases:
phpsploit_pipe alias > $TMPFILE
sed -e '1,/---/d' -e '/^$/,$d' $TMPFILE | grep -vq '^    l' || FAIL

# check that alias is equal to it's original command
phpsploit_pipe alias "'@foo.bar'" lrun ls > $TMPFILE || FAIL
phpsploit_pipe @foo.bar --color=always -1 / > $TMPFILE-alias || FAIL
phpsploit_pipe lrun ls --color=always -1 / > $TMPFILE || FAIL
diff $TMPFILE-alias $TMPFILE || FAIL

# commands & plugins can be overridden by aliases
phpsploit_pipe alias lrun "exploit --get-backdoor" > $TMPFILE
phpsploit_pipe lrun > $TMPFILE-cmd-override
phpsploit_pipe exploit --get-backdoor > $TMPFILE || FAIL
diff $TMPFILE-cmd-override $TMPFILE || FAIL

# but the alias referencing `lrun` still uses real command
# because phpsploit nested aliases do not exist in phpsploit:
phpsploit_pipe @foo.bar --color=always -1 / > $TMPFILE || FAIL
diff $TMPFILE-alias $TMPFILE || FAIL

# thanks to non-nesting, you can alias ls to 'ls /'
# without circular calling issue:
phpsploit_pipe alias ls ls /etc > $TMPFILE || FAIL
phpsploit_pipe exploit > $TMPFILE || FAIL
phpsploit_pipe ls > $TMPFILE-alias || FAIL
# remove that alias, and `ls` becomes `ls` again !
phpsploit_pipe alias ls None > $TMPFILE || FAIL
assert_contains $TMPFILE '`ls` alias correctly deleted'
# now that ls is real `ls`, it should have different output:
phpsploit_pipe ls > $TMPFILE || FAIL
diff $TMFILE-alias $TMPFILE > $TMPFILE-err && FAIL
rm $TMPFILE-err
# but calling `ls / gives same output as previous call to `ls` alias:
phpsploit_pipe ls /etc > $TMPFILE
diff $TMPFILE-alias $TMPFILE || FAIL


###
### CHECK INVALID ALIAS NAMES
###

# keep track of previously existing aliases
phpsploit_pipe alias > $TMPFILE-ref || FAIL

# issue #101: crash: IndexError: list index out of range
# empty string fails
phpsploit_pipe 'alias "" BLA' > $TMPFILE && FAIL
assert_contains $TMPFILE "\[\!\] Key Error: illegal name: '' doesn't match \[A-Za-z0-9@_\.-\]+"
# string with spaces fails
phpsploit_pipe 'alias "has space" BLA' > $TMPFILE && FAIL
assert_contains $TMPFILE "\[\!\] Key Error: illegal name: 'has space' doesn't match \[A-Za-z0-9@_\.-\]+"
# ',' (badchar) fails
phpsploit_pipe 'alias ,bad BLA' > $TMPFILE && FAIL
assert_contains $TMPFILE "\[\!\] Key Error: illegal name: ',bad' doesn't match \[A-Za-z0-9@_\.-\]+"

# ensure alias output hasn't changed (because no vars were created)
phpsploit_pipe alias > $TMPFILE || FAIL
diff $TMPFILE-ref $TMPFILE
