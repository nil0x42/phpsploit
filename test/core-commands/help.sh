#!/usr/bin/env bash

###
### help
###
$PHPSPLOIT -e 'exploit; help' > $TMPFILE || FAIL
grep -q "^Core Commands" $TMPFILE || FAIL
grep -q "^Command Aliases" $TMPFILE || FAIL
grep -q "^System Plugins" $TMPFILE || FAIL

# if not connected (`exploit`), plugins are not listed
phpsploit_pipe help > $TMPFILE || FAIL
grep -q "^Core Commands" $TMPFILE || FAIL
grep -q "^Command Aliases" $TMPFILE || FAIL
grep -q "^System Plugins" $TMPFILE && FAIL


###
### help <CORE-COMMAND>
###
core_cmds=`grep -oP '(?<=def do_)[a-z]+(?=\()' $ROOTDIR/src/ui/interface.py`
for cmd in $core_cmds; do
    phpsploit_pipe help $cmd > $TMPFILE || FAIL

    grep -q "^\[\*\] $cmd: " $TMPFILE || FAIL
    grep -q "^SYNOPSIS:" $TMPFILE || FAIL

    # min docstring lines (debug line removed)
    [ `grep -vc '^\[\#' $TMPFILE` -lt 10 ] && FAIL

    echo "[OK] help $cmd"
done


###
### help <PLUGIN>
###
plugins=`find $ROOTDIR/plugins/*/* -maxdepth 0 -exec basename {} ';'`
for plugin in $plugins; do
    phpsploit_pipe help $plugin > $TMPFILE || FAIL

    grep -q "^\[\*\] $plugin: " $TMPFILE || FAIL
    grep -q "^SYNOPSIS:" $TMPFILE || FAIL
    grep -q "^DESCRIPTION:" $TMPFILE || FAIL

    echo "[OK] help $plugin"
done


###
### help <ALIAS>
###
$PHPSPLOIT -e 'alias' > $TMPFILE || FAIL
cmds=`sed -e '1,/---/d' -e '/^$/,$d' $TMPFILE | awk '{print $1}'`
for cmd in $cmds; do

    # check that `help <ALIAS>` == `alias <ALIAS`
    phpsploit_pipe help $cmd > $TMPFILE || FAIL
    grep -v '^\[\#' $TMPFILE > $TMPFILE-1

    phpsploit_pipe alias $cmd > $TMPFILE || FAIL
    grep -v '^\[\#' $TMPFILE > $TMPFILE-2

    diff $TMPFILE-1 $TMPFILE-2 || FAIL

    echo "[OK] help $cmd"
done
rm $TMPFILE*


###
### help set <SETTING>
###
settings=`phpsploit_pipe set | grep -E '^    [A-Z]{2,}' | awk '{print $1}'`
for var in $settings; do
    phpsploit_pipe help set $var > $TMPFILE || FAIL

    # issue #67:  `help set <VAR>`: display buffer type description
    # Ref: https://github.com/nil0x42/phpsploit/issues/67
    # check that all settings help have a buffer description
    grep -Eq "$var is a (Multi|Rand)LineBuffer." $TMPFILE || FAIL

    # make sure a setting description is available
    desc_lines=`sed -e '1,/^[A-Z]\+/d' -e '/^[A-Z]\+/,$d' $TMPFILE | wc -l`
    [ $desc_lines -lt 2 ] && FAIL

    echo "[OK] help set $var"
done


###
### help <COMMAND> <ARG>
###
# issue #70: get help for `CMD` when calling `help CMD ARG`
# Ref: https://github.com/nil0x42/phpsploit/issues/70
# ensure this gives help for `corectl`:
phpsploit_pipe help corectl FOOBAR > $TMPFILE || FAIL
grep -q '^\[\*\] corectl: ' $TMPFILE || FAIL


###
### Check invalid commands
###
# check output
phpsploit_pipe help FOO BAR > $TMPFILE && FAIL
grep -q '^\[\-\] No help for: FOO' $TMPFILE || FAIL
