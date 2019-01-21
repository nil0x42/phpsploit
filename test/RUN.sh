#!/bin/bash

# RUN.sh:
#   Run a test script or all tests contained in
#   a given directory, in a recursive manner.




BANNER=$(perl -E 'print "="x79 . "\r\t\t"')

function print_info () {
    echo -e "\033[1;34m[*]\033[0;36m $1\033[0m"
}
function print_good () {
    echo -e "\033[1;32m[+]\033[0;32m $1\033[0m"
}
function print_bad () {
    echo -e "\033[1;31m[-]\033[0;31m $1\033[0m"
}

function print_inf2 () {
    str="$1"
    colored=" = \033[0;35m"
    str="${str/\=/$colored}"
    echo -e "\033[1;33m[I]\033[0;33m $str\033[0m"
}


if [ -n "$PHPSPLOIT_TEST" ]; then
    yel="\033[0;34m"
    print_inf2 "Script Context:"
    print_inf2 "    PWD=$PWD"
    print_inf2 "    ROOTDIR=$ROOTDIR"
    print_inf2 "    TESTDIR=$TESTDIR"
    print_inf2 "    TMPDIR=$TMPDIR"
    print_inf2 "    TMPFILE=$TMPFILE"
    print_inf2 "Phpsploit Context:"
    print_inf2 "    PHPSPLOIT=$PHPSPLOIT"
    print_inf2 "    PHPSPLOIT_CONFIG_DIR=$PHPSPLOIT_CONFIG_DIR"
    print_inf2 "PHP Server Context:"
    print_inf2 "    WWWROOT=$WWWROOT"
    print_inf2 "    TARGET=$TARGET"
    set -ve
    . "$1"
    exit 0
fi
export PHPSPLOIT_TEST=1

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
export TESTDIR="$(realpath `dirname $0`)"
# testscript = /phpsploit/test/RUN.sh
testscript="$(realpath $0)"

# TMPDIR = /phpsploit/test/tmp/
export TMPDIR="$TESTDIR/tmp"
rm -rf "$TMPDIR"
mkdir "$TMPDIR"

# PHPSPLOIT_CONFIG_DIR = /phpsploit/test/tmp/phpsploit-config/
export PHPSPLOIT_CONFIG_DIR="$TMPDIR/phpsploit-config"
mkdir "$PHPSPLOIT_CONFIG_DIR"
cat "$ROOTDIR/data/config/config" > "$PHPSPLOIT_CONFIG_DIR/config"

# PHPSPLOIT = call phpsploit abspath (uses PHPSPLOIT_CONFIG_DIR)
export PHPSPLOIT="$ROOTDIR/phpsploit"

###
### build temp php server to be able to run 'exploit'
###
# TARGET = 127.0.0.1:PORT
export TARGET="127.0.0.1:$(( ( RANDOM ) + 30000 ))"

# WWWROOT = /phpsploit/test/tmp/wwwroot/
export WWWROOT="$TMPDIR/wwwroot"
mkdir "$WWWROOT"
$PHPSPLOIT -e 'exploit --get-backdoor' > "$WWWROOT/index.php"
echo "set TARGET $TARGET" >> "$PHPSPLOIT_CONFIG_DIR/config"
# run php server (killed on atexit())
nohup php -S "$TARGET" -t "$WWWROOT" > "$WWWROOT/php.log" 2>&1 &
srv_pid=$!


# called at script exit
function atexit () {
    # kill php server
    [ -n "$srv_pid" ] && kill $srv_pid
}
trap atexit EXIT


tests=0
errors=0

# run a single test script _bash)
# NOTE: only launched if is executable (chmod +x)
function execute_script () {
    if [ -f "$1" -a -x "$1" -a "`realpath $1`" != "`realpath $0`" ]; then
        print_info "$BANNER"
        print_info "RUNNING $1 ..."
        print_info "$BANNER"

        # do script context
        export SCRIPTDIR="$(realpath `dirname $1`)"
        cd "$SCRIPTDIR"
        export TMPFILE=`mktemp`

        if bash "$testscript" "$1"; then
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
    if [[ "`realpath $1`" != "$TESTDIR"/* ]]; then
        >&2 echo "Invalid test location: $1"
        exit 1
    fi
    execute_scripts "$1"
else
    exit_help
fi

echo
if [ $errors -eq 0 ]; then
    print_info "$BANNER TESTS SUMMARY "
    print_info "All tests ($tests) succeeded! "
    print_info "$BANNER\n"
    exit 0
else
    print_bad "$BANNER TESTS SUMMARY "
    print_bad "Some tests ($errors/$tests) failed! "
    print_bad "$BANNER\n"
    exit 1
fi
