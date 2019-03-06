#!/usr/bin/env bash

############################################################
### NON-CONNECTED
###     we have never been connected to a target
############################################################

# issue #53: env: Confusing error message before `exploited` context
# Ref: https://github.com/nil0x42/phpsploit/issues/53
phpsploit_pipe env > $TMPFILE && FAIL
grep -q '^\[\-\] Must connect to spread env vars ' $TMPFILE || FAIL
phpsploit_pipe env PWD > $TMPFILE && FAIL
grep -q '^\[\-\] Must connect to spread env vars ' $TMPFILE || FAIL


############################################################
### CONNECTED
###     we are currently connected to target (`exploit`)
############################################################
phpsploit_pipe exploit > $TMPFILE || FAIL

# env must succesfully return list of env vars after exploited
phpsploit_pipe env > $TMPFILE || FAIL

# list of all env vars
env_vars=`sed -e '1,/---/d' -e '/^$/,$d' $TMPFILE | awk '{print $1}'`

# keep clean output for comparison
grep -v '^\[\#' $TMPFILE > $TMPFILE-1


############################################################
### DISCONNECTED
###     we disconnected from target (`exit`)
############################################################
phpsploit_pipe exit > $TMPFILE || FAIL

# env must succesfully return list of env vars, even after disconnect
phpsploit_pipe env > $TMPFILE || FAIL
# keep clean output for comparison
grep -v '^\[\#' $TMPFILE > $TMPFILE-2

# compare env connected, with env after disconnection
diff $TMPFILE-1 $TMPFILE-2 || FAIL
rm $TMPFILE-1 $TMPFILE-2


###
### env <VAR>
###
# list of readonly env vars
getval () {
    phpsploit_pipe env $1 > $TMPFILE-getval
    grep -oP '^\s+'$1'+\s+\K.*(?=\s*$)' $TMPFILE-getval
}
ro_env=" ADDR CLIENT_ADDR HOST HTTP_SOFTWARE PATH_SEP PHP_VERSION WEB_ROOT "
for var in $env_vars; do
    phpsploit_pipe env $var > $TMPFILE || FAIL
    old_val="`getval $var`"
    [ -z "$old_val" ] && FAIL

    # if var is readonly
    if [[ "$ro_env" == *" $var "* ]]; then

        # try to set another value (must fail)
        phpsploit_pipe env $var FOOBAR > $TMPFILE && FAIL
        grep -q "'$var' variable is read-only" $TMPFILE || FAIL
        [[ "`getval $var`" == "$old_val" ]] || FAIL

        # try to unset variable (must fail)
        phpsploit_pipe "env $var none" > $TMPFILE && FAIL
        [[ "`getval $var`" == "$old_val" ]] || FAIL

    # else
    else

        ## try to set another value (must succeed)
        phpsploit_pipe env $var FOOBAR > $TMPFILE || FAIL
        [[ "`getval $var`" == "FOOBAR" ]] || FAIL

        # try to unset variable (must succeed)
        phpsploit_pipe "env $var none" > $TMPFILE || FAIL
        [ -z "`getval $var`" ] || FAIL

    fi
    echo "[OK] env $var"
done


###
### CHECK VALID VAR NAMES
###   (create new custom env vars)
###

phpsploit_pipe env FOO BAR > $TMPFILE || FAIL
[[ "`getval FOO`" == "BAR" ]] || FAIL

phpsploit_pipe env this@IS.valid myval > $TMPFILE || FAIL
[[ "`getval this@IS.valid`" == "myval" ]] || FAIL

###
### CHECK INVALID VAR NAMES
###

# keep track of previously existing env vars
phpsploit_pipe env > $TMPFILE-ref || FAIL

# empty string fails
phpsploit_pipe 'env "" BLA' > $TMPFILE && FAIL
assert_contains $TMPFILE "\[\!\] Key Error: illegal name: '' doesn't match \[A-Za-z0-9@_\.-\]+"
# string with spaces fails
phpsploit_pipe 'env "has space" BLA' > $TMPFILE && FAIL
assert_contains $TMPFILE "\[\!\] Key Error: illegal name: 'has space' doesn't match \[A-Za-z0-9@_\.-\]+"
# ',' (badchar) fails
phpsploit_pipe 'env ,bad BLA' > $TMPFILE && FAIL
assert_contains $TMPFILE "\[\!\] Key Error: illegal name: ',bad' doesn't match \[A-Za-z0-9@_\.-\]+"
# special name used to save default values in sessions, should fail
phpsploit_pipe 'env __DEFAULTS__ BLA' > $TMPFILE && FAIL
assert_contains $TMPFILE "\[\!\] Key Error: illegal name: '__DEFAULTS__'"

# ensure env output hasn't changed (because no vars were created)
phpsploit_pipe env > $TMPFILE || FAIL
diff $TMPFILE-ref $TMPFILE
