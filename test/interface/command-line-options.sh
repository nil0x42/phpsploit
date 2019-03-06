#!/bin/bash

# ARGV1: long cli option name (e.g: --eval)
# ARGV2: optional value for argument
#
# FAIL if $retval or STDOUT differ when using argument's different forms.
#   short:   '-e $value'
#   long:    '--eval $value'
#   long_eq: '--eval=$value'
function test_opt () {
    local short_opt="-${1:2:1}"
    local long_opt="$1"
    local value="$2"

    if [ -z "$value" ]; then
        echo exit | $PHPSPLOIT $short_opt > $TMPFILE-test_opt-short
        local ret1=$?
        echo exit | $PHPSPLOIT $long_opt > $TMPFILE-test_opt-long
        local ret2=$?

        [ "$ret1" == "$ret2" ] || FAIL
        diff $TMPFILE-test_opt-short $TMPFILE-test_opt-long || FAIL
    else
        echo exit | $PHPSPLOIT $short_opt "$value" > $TMPFILE-test_opt-short
        local ret1=$?
        echo exit | $PHPSPLOIT $long_opt "$value" > $TMPFILE-test_opt-long
        local ret2=$?
        echo exit | $PHPSPLOIT "$long_opt=$value" > $TMPFILE-test_opt-long_eq
        local ret3=$?

        [ "$ret1" == "$ret2" ] || FAIL
        diff $TMPFILE-test_opt-short $TMPFILE-test_opt-long || FAIL
        [ "$ret2" == "$ret3" ] || FAIL
        diff $TMPFILE-test_opt-long $TMPFILE-test_opt-long_eq || FAIL
    fi
    # output result
    cat $TMPFILE-test_opt-short
    # store return value into $retval
    retval="$ret1"
    # remove files used by function
    rm -f $TMPFILE-test_opt-*
    return "$retval"
}

# make sure ARGV1 file outputs standard argparse cli error
function assert_cli_error () {
assert_contains $1 << EOF
^usage: phpsploit 
^phpsploit: error: 
EOF
}

# return 0 if command timed-out (aka: is interactive)
function is_interactive () {
    local script=$TMPFILE-is_interactive.sh
    echo -e "#!/bin/bash\n$@" > $script
    chmod +x $script
    script -qefc "timeout 6 $script" /dev/null > $TMPFILE-is_interactive 2>&1
    local ret="$?"
    #rm $script
    [ "$ret" -eq 124 ] && return 0 || return 1
}


###
### --help
###
is_interactive $PHPSPLOIT --help && FAIL

$PHPSPLOIT --help=INVALID 2> $TMPFILE && FAIL
assert_contains $TMPFILE << EOF
usage: .*phpsploit
--help: ignored explicit argument 'INVALID'
EOF

test_opt --help > $TMPFILE || FAIL
assert_contains $TMPFILE << EOF
optional arguments:
  -h, --help
  -v, --version
  -c <FILE>, --config <FILE>
  -l <SESSION>, --load <SESSION>
  -t <URL>, --target <URL>
  -s <FILE>, --source <FILE>
  -e <CMD>, --eval <CMD>
  -i, --interactive
EOF

### ensure all options are being tested in current test file
options="$(grep -- -- $TMPFILE | perl -pe 's|(^.*--(.*?) .*$)|\2|')"
for opt in $options; do
    assert_contains $SCRIPTFILE "^test_opt --$opt "
    assert_contains $SCRIPTFILE "^is_interactive \$PHPSPLOIT --$opt "
done


###
### --version
###
is_interactive $PHPSPLOIT --version && FAIL

test_opt --version > $TMPFILE || FAIL
assert_contains $TMPFILE << EOF
^PhpSploit Framework, version 
^License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
^This is free software; you are free to change and redistribute it.
^There is NO WARRANTY, to the extent permitted by law.
EOF

# FAIL if option has argument
test_opt --version INVALID 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE


###
### --config
###

### succeed with VALID conf file
cat > $TMPFILE-conf << EOF
# valid comment
  # valid comment
alias test_alias 'lrun true' # valid comment
set EDITOR test_set
EOF

is_interactive $PHPSPLOIT --config $TMPFILE-conf || FAIL

# check existence of newly created alias
test_opt --config $TMPFILE-conf > $TMPFILE || FAIL
$PHPSPLOIT -c $TMPFILE-conf -e 'alias' > $TMPFILE
assert_contains $TMPFILE << EOF
 test_alias .* lrun true$
EOF
# check that original $PHPSPLOIT_CONFIG_DIR is NOT loaded
num_aliases=$(sed -e '1,/---/d' -e '/^$/,$d' $TMPFILE | wc -l)
[ "$num_aliases" == 1 ] || FAIL # only declared `test_alias` should exist

# check existence of newly created setting
$PHPSPLOIT -c $TMPFILE-conf -e 'set' > $TMPFILE
assert_contains $TMPFILE << EOF
 EDITOR .* test_set$
EOF

### FAIL with INVALID conf file
cat > $TMPFILE-conf << EOF
# valid comment
  # valid comment
alias test_alias 'lrun true' # valid comment
session load / # THIS COMMAND SHOULD FAIL
set EDITOR test_set
EOF

test_opt --config $TMPFILE-conf > /dev/null 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE

rm $TMPFILE-conf

### FAIL if called without value
test_opt --config 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE


###
### --load
###

### succeed with VALID session file
$PHPSPLOIT -e "exploit; env TEST_ENV FOOBAR; session save $TMPFILE-sess" > $TMPFILE || FAIL
assert_contains $TMPFILE << EOF
Session saved into '$TMPFILE-sess'
EOF

is_interactive $PHPSPLOIT --load $TMPFILE-sess || FAIL

# test option
test_opt --load $TMPFILE-sess > /dev/null || FAIL
# check session is loaded
$PHPSPLOIT -l $TMPFILE-sess -e "session" > $TMPFILE
assert_contains $TMPFILE << EOF
Configuration Settings
Environment Variables
TEST_ENV .* FOOBAR$
EOF
# compare --load option with 'session load' command
$PHPSPLOIT -e "session load $TMPFILE-sess; session" > $TMPFILE-2
diff $TMPFILE $TMPFILE-2 || FAIL

### FAIL with INVALID session file
echo "INVALID SESSION FILE CONTENT" > $TMPFILE-sess || FAIL
# test option
test_opt --load $TMPFILE-sess > /dev/null 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE

rm $TMPFILE-sess $TMPFILE-2

### FAIL if called without value
test_opt --load 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE


###
### --target
###

is_interactive $PHPSPLOIT --target localhost || FAIL

### succeed with VALID target
# test option
TARGET="10.0.156.11:8080"
test_opt --target $TARGET > /dev/null || FAIL
# check target is set
$PHPSPLOIT -t $TARGET -e "set" > $TMPFILE
assert_contains $TMPFILE << EOF
 TARGET .* http://$TARGET/$
EOF

### FAIL if called with INVALID target
test_opt --target / > /dev/null 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE

### FAIL if called without argument
test_opt --target > /dev/null 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE


###
### --source
###

### succeed with VALID source file (even with an invalid command in the middle)
cat > $TMPFILE-src << EOF
# valid comment
  # valid comment
alias test_alias 'lrun true' # valid comment
INVALID_COMMAND # this command should fail
set EDITOR test_set
EOF

is_interactive $PHPSPLOIT --source $TMPFILE-src && FAIL

# check existence of newly created alias
test_opt --source $TMPFILE-src > $TMPFILE || FAIL
$PHPSPLOIT -s $TMPFILE-src -e 'alias' > $TMPFILE
assert_contains $TMPFILE << EOF
 test_alias .* lrun true$
EOF
# check that original $PHPSPLOIT_CONFIG_DIR IS loaded
num_aliases=$(sed -e '1,/---/d' -e '/^$/,$d' $TMPFILE | wc -l)
[ "$num_aliases" -gt 1 ] || FAIL # aliases set by conf file should also exist

# check existence of newly created setting
$PHPSPLOIT -s $TMPFILE-src -e 'set' > $TMPFILE
assert_contains $TMPFILE << EOF
 EDITOR .* test_set$
EOF

# FAIL if called with non-existing source file
test_opt --source INVALID > /dev/null 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE

rm $TMPFILE-src

### FAIL if called without value
test_opt --source 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE


###
### --eval
###

is_interactive $PHPSPLOIT --eval help && FAIL

### succeed if called with multiple valid commands
test_opt --eval 'set; alias' > $TMPFILE
assert_contains $TMPFILE << EOF
^Configuration Settings$
^Command Aliases$
EOF

### FAIL if called without value
test_opt --eval 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE


###
### --interactive
###

cat > $TMPFILE-src << EOF
# valid comment
  # valid comment
alias test_alias 'lrun true' # valid comment
INVALID_COMMAND # this command should fail
set EDITOR test_set
EOF
is_interactive $PHPSPLOIT --interactive --source $TMPFILE-src || FAIL
rm $TMPFILE-src

is_interactive $PHPSPLOIT --interactive --eval help || FAIL

is_interactive $PHPSPLOIT --interactive --target localhost || FAIL

# check stdin correctly interpreted
echo exit | $PHPSPLOIT --interactive -e 'set; alias' > $TMPFILE
assert_contains $TMPFILE << EOF
^Configuration Settings$
^Command Aliases$
EOF

### FAIL if called with argument
test_opt --interactive INVALID 2> $TMPFILE && FAIL
assert_cli_error $TMPFILE
