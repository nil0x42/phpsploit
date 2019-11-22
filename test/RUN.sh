#!/bin/bash

# RUN.sh:
#   Run a test script or all tests contained in
#   a given directory, in a recursive manner.


#####
# THIS CODE IS EXECUTED WHEN THIS SCRIPT
# IS CALLED TO RUN A SINGLE TEST (from function execute_script())
#####
function print_info () {
    echo -e "\033[0m\033[1;34m[*]\033[0;36m $@\033[0m"
}
function print_good () {
    echo -e "\033[0m\033[1;32m[+]\033[0;32m $@\033[0m"
}
function print_bad () {
    echo -e "\033[0m\033[1;31m[-]\033[0;31m $@\033[0m"
}
function FAIL () {
    set +v
    local file="${BASH_SOURCE[1]}"
    local lineno=$BASH_LINENO
    local line="$(sed -n ${BASH_LINENO}p "${BASH_SOURCE[1]}")"

    print_bad "\033[1;31m"============================================================
    print_bad "\033[1;31mTEST FAILED\033[0;31m"
    print_bad "\033[1;31mFILE:\033[0;31m $file:$lineno"
    print_bad "\033[1;31mLINE:\033[0;31m $line"
    if [ $# -gt 0 ]; then
        # local repr=$(grep -oP "(?<= FAIL ).+"
        local repr="${line##* FAIL }"
        print_bad "\033[1;31m$repr:\033[0;31m $@"
    fi
    exit 1
}
function print_env () {
    [ -z "${!1}" ] && return
    echo -e "\033[0m\033[1;33m[I]    \033[0;33m$1\033[0m = \033[1;33m${!1}\033[0m"
}
function faketty () {
    # for some strange reason, `script` sets CRLF as newlines,
    # so we remove them with perl
    script -qefc "$(printf "%q " "$@")" /dev/null | \
        perl -pe 's/\r\n/\n/'
}
# FAIL if any STDIN line can't be found in ARGV1 file
#   - if ARGV2 exists, it's used instead of STDIN
function assert_contains () {
    if [ -n "$2" ]; then
        local match="$2"
        grep -q -- "$match" "$1" || FAIL $match / $1
    else
        while IFS= read -r match; do
            grep -q -- "$match" "$1" || FAIL $match / $1
        done
    fi
}
# FAIL if any STDIN line is present in ARGV1 file
#   - if ARGV2 exists, it's used instead of STDIN
function assert_not_contains () {
    if [ -n "$2" ]; then
        local match="$2"
        ! grep -q -- "$match" "$1" || FAIL $match / $1
    else
        while IFS= read -r match; do
            ! grep -q -- "$match" "$1" || FAIL $match / $1
        done
    fi
}
# FAIL if ARGV1 file has some output other than debug '[#]' lines
function assert_no_output () {
    [ -f "$1" ] || FAIL "file does not exist" / $1
    grep -qv '\[\#\]' $1 && FAIL "file has some output" / $1
}
# remove ANSI colors from ARGV1 file
function decolorize () {
    sed -ri "s/\x01?\x1B\[(([0-9]+)(;[0-9]+)*)?m\x02?//g" "$1"
}
function exit_script () {
    ret=$?
    if [ -n "$__phpsploit_pipe_pid" ]; then
        # cannot just kill phpsploit pipe, or coveragepy will not write report
        echo -e "\nexit --force\nexit --force\nexit --force" >&8
        for ((n=0;n<20;n++)); do
            sleep 0.2
            ps -ef | grep -v grep | grep -q " $__phpsploit_pipe_pid " || break
        done
        errmsg="phpsploit_pipe process $__phpsploit_pipe_pid didn't quit normally: missing coverage report"
        ps -ef | grep -v grep | grep " $__phpsploit_pipe_pid " && FAIL $errmsg
        if [ -n "$COVERAGE" ]; then
            [ -f $ROOTDIR/.coverage.*.$__phpsploit_pipe_pid.* ] || FAIL $errmsg
        fi
    fi
    [ $ret -eq 0 ] && return # ignore if return value == 0
    files=$(find $TMPDIR -type f -name "`basename $TMPFILE`"'*')
    for file in $files; do
        varname="${file/$TMPFILE/\$TMPFILE}"
        print_bad "\033[1;31m"------------------------------------------------------------
        print_bad "\033[1;31mcat $varname\033[0;31m ($file):"
        cat "$file"
    done
    # tail -n+1 /dev/null $files | tail -n+3
}
function phpsploit_pipe () {
    if [ -z "$__phpsploit_pipe_pid" ]; then
        # singleton, start piped phpsploit first time function is called
        rm -f $TMPDIR/fifo-in $TMPDIR/fifo-out
        mkfifo $TMPDIR/fifo-in $TMPDIR/fifo-out
        exec 8<>$TMPDIR/fifo-in
        exec 9<>$TMPDIR/fifo-out
        $PHPSPLOIT <&8 >&9 2>&1 &
        __phpsploit_pipe_pid=$!
    fi
    randstr=`cat /dev/urandom | tr -dc A-Za-z0-9 | head -c 13`
    buf=$TMPDIR/buffer
    echo -e "$@" >&8
    echo "@lrun echo $randstr" >&8 # delimiter
    head -c 1 <&9 > $buf
    while ! grep -q "$randstr.*Returned " $buf; do
        timeout 0.05 cat <&9 >> $buf
    done
    sed -i "/$randstr/d" $buf
    cat $buf
    # try to get retval from last cmd (needs VERBOSITY True)
    ret=`tail -n1 $buf | grep '^\[\#.*eturned [0-9]\+' | awk '{print $NF}'`
    [ -n "$ret" ] && return $ret
}
# remove debug lines from input (phpsploit lines starting with '[#'
function nodebug () {
    grep -v '^\[\#'
}
# count lines (after removing empty & debug lines)
function count_lines () {
    cat $1 | nodebug | grep -v '^$' | wc -l
}
if [ -n "$PHPSPLOIT_TEST" ]; then
    trap exit_script EXIT
    print_env PWD
    print_env ROOTDIR
    print_env TESTDIR
    print_env SCRIPTDIR
    print_env SCRIPTFILE
    print_env TMPDIR
    print_env TMPFILE
    print_env PHPSPLOIT
    print_env PHPSPLOIT_CONFIG_DIR
    print_env RAW_PHPSPLOIT
    print_env WWWROOT
    print_env TARGET
    print_env COVERAGE
    print_env COVERAGE_FILE
    print_env COVERAGE_RCFILE
    set -v
    # execute the `real` test script
    . "$1" || true
    exit 0
fi
export PHPSPLOIT_TEST=1



#####
# MAIN TEST LAUNCHER
#####
set -e


# change color of stderr output
colored_stderr()(set -o pipefail;"$@" 2>&1>&3|sed $'s,.*,\e[33;2m&\e[m,'>&2)3>&1

# check dependencies
errors=0
function check_dependency () {
    if ! which "$1" >/dev/null; then
        print_bad "Missing dependency: $1"
        (( ++errors ))
    fi
}
check_dependency basename
check_dependency bash
check_dependency diff
check_dependency dirname
check_dependency git
check_dependency grep
check_dependency md5sum
check_dependency nohup
check_dependency perl
check_dependency php
check_dependency printf
check_dependency readlink
check_dependency script
check_dependency tail
check_dependency tee
check_dependency timeout
[ $errors -eq 0 ] || exit 1


function exit_help () {
    >&2 echo "$0:"
    >&2 echo "  Run a single test, or recursively run all"
    >&2 echo "  tests contained in a test directory."
    >&2 echo ""
    >&2 echo "Usage: $0 <tests-file>"
    >&2 echo "       $0 <tests-directory>"
    exit 1
}


# ROOTDIR = /phpsploit/
export ROOTDIR="$(git rev-parse --show-toplevel)"

# TESTDIR = /phpsploit/test/
export TESTDIR="$(readlink -f `dirname $0`)"
# testscript = /phpsploit/test/RUN.sh
testscript="$(readlink -f $0)"

# TMPDIR = /phpsploit/test/tmp/
export TMPDIR="$TESTDIR/tmp"
rm -rf "$TMPDIR"
mkdir "$TMPDIR"

# PHPSPLOIT_CONFIG_DIR = /phpsploit/test/tmp/phpsploit-config/
export PHPSPLOIT_CONFIG_DIR="$TMPDIR/phpsploit-config"
mkdir "$PHPSPLOIT_CONFIG_DIR"
cat "$ROOTDIR/data/config/config" > "$PHPSPLOIT_CONFIG_DIR/config"
echo "set VERBOSITY True" >> "$PHPSPLOIT_CONFIG_DIR/config"
echo "set REQ_INTERVAL 0" >> "$PHPSPLOIT_CONFIG_DIR/config" # make multireq faster
echo "alias true 'lrun true'" >> "$PHPSPLOIT_CONFIG_DIR/config"
echo "alias @lrun lrun" >> "$PHPSPLOIT_CONFIG_DIR/config"

# PHPSPLOIT = call phpsploit abspath (uses PHPSPLOIT_CONFIG_DIR)
export RAW_PHPSPLOIT="$ROOTDIR/phpsploit"
export PHPSPLOIT="$ROOTDIR/phpsploit"
# add 'coverage run' prefix if $COVERAGE is set
if [ -n "$COVERAGE" ]; then
    export COVERAGE_RCFILE="$ROOTDIR/.coveragerc"
    export COVERAGE_FILE="$ROOTDIR/.coverage"
    rm -f $COVERAGE_FILE $COVERAGE_FILE.*
    export PHPSPLOIT="coverage run --rcfile=$COVERAGE_RCFILE $PHPSPLOIT"
fi

###
### build temp php server to be able to run 'exploit'
###
# TARGET = 127.0.0.1:PORT
export TARGET="127.0.0.1:$(( ( RANDOM ) + 30000 ))"

# WWWROOT = /phpsploit/test/tmp/wwwroot/
export WWWROOT="$TMPDIR/wwwroot"
mkdir "$WWWROOT"
$PHPSPLOIT -e 'exploit --get-backdoor' > "$WWWROOT/index.php"
chmod +x "$WWWROOT/index.php"
echo "set TARGET $TARGET" >> "$PHPSPLOIT_CONFIG_DIR/config"

# run php server (killed on atexit())
php -S "$TARGET" -t "$WWWROOT" > "$WWWROOT/php.log" 2>&1 &
srv_pid=$!
sleep 2 # give php server some time to init properly


# called at script exit
function atexit () {
    # kill php server
    [ -n "$srv_pid" ] && kill $srv_pid
}
trap atexit EXIT


tests=0
errors=0
banner()(python -c 'print("'"$1"'".center(70, "="))')


# run a single test script _bash)
# NOTE: only launched if is executable (chmod +x)
function execute_script () {
    if [ -f "$1" -a -x "$1" -a "`readlink -f $1`" != "`readlink -f $0`" ]; then
        print_info "`banner`"
        print_info "RUNNING $1 ..."
        print_info "`banner`"

        # do script context
        export SCRIPTDIR="$(readlink -f `dirname $1`)"
        cd "$SCRIPTDIR"
        export SCRIPTFILE="$(readlink -f $1)"
        export TMPFILE=`mktemp`

        #if colored_stderr stdbuf -oL bash "$testscript" "$1"; then
        if colored_stderr bash "$testscript" "$1"; then
            print_good "$1 succeeded"
        else
            print_bad "$1 failed !"
            (( ++errors ))
        fi

        # undo script context
        cd - > /dev/null

        echo -e "\n"
        (( ++tests ))
    fi
}

# recursively run all tests in test directory
function execute_scripts () {
    basename="`basename $1`"
    if [ "$basename" == "tmp" ]; then
        return
    fi
    if [ -d "$1" ]; then
        for i in "$1"/*; do
            execute_scripts "$i"
        done
    else
        execute_script "$1"
    fi
}


if [ "$1" == '-h' -o "$1" == '--help' ]; then
    exit_help
fi


if [ $# -eq 0 ]; then
    execute_scripts "$TESTDIR"
elif [ $# -eq 1 ]; then
    if [ ! -r "$1" ]; then
        >&2 echo "No such file or directory: $1"
        exit 1
    fi
    if [[ "`readlink -f $1`" != "$TESTDIR"/* ]]; then
        >&2 echo "Invalid test location: $1"
        exit 1
    fi
    execute_scripts "`readlink -f $1`"
else
    exit_help
fi

echo
if [ -n "$COVERAGE" ]; then
    cd $ROOTDIR
    echo 'find -name ".coverage\.*"'
    find -name ".coverage\.*"
    coverage combine
    cd - > /dev/null
fi
if [ $errors -eq 0 ]; then
    print_info "`banner ' TESTS SUMMARY '`"
    print_info "All tests ($tests) succeeded! "
    print_info "`banner`"
    echo
    exit 0
else
    printf '\e[33;2m' # same color as in colored_stderr()
    echo 'ps -fP $srv_pid'
    ps -fP $srv_pid
    echo 'cat "$WWWROOT/php.log"'
    cat "$WWWROOT/php.log"

    print_bad "`banner ' TESTS SUMMARY '`"
    print_bad "Some tests ($errors/$tests) failed! "
    print_bad "`banner`"
    echo
    exit 1
fi
