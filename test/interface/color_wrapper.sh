#!/bin/bash

# check color rendering of output wrapper

SCRIPTDIR="$(realpath `dirname $0`)"
cd `git rev-parse --show-toplevel`

echo $SCRIPTDIR

set -ve

function faketty () {
    script -eqc "$1" /dev/null
}

cmd="./phpsploit -c 'data/config/config' -s '$SCRIPTDIR/color_wrapper.src'"

# check raw output integrity
raw_output=`$cmd`
echo "$raw_output"
raw_output_md5=`echo "$raw_output"     | md5sum | cut -d' ' -f1`
echo "$raw_output_md5"
[ "$raw_output_md5" == "1d48c0290f788400ae6d729d68d12802" ]

# check colored output integrity
colored_output=`faketty "$cmd"`
echo "$colored_output"
colored_output_md5=`echo "$colored_output" | md5sum | cut -d' ' -f1`
echo "$colored_output_md5"
[ "$colored_output_md5" == "8ab9ff0d849195ecbcb6ca2a1834eab0" ]
