# vi: ft=sh

cd `git rev-parse --show-toplevel`

SCRIPTDIR="$(realpath `dirname $0`)"

SRV_ADDR="127.0.0.1:64957"
SRV_WEBDIR="/tmp/phpsploit-test-server/"
SRV_PIDFILE="$SRV_WEBDIR/server.pid"


# run a phpsploit test given a phpsploit source file
function run_phpsploit_test () {
    ./phpsploit \
        --config ./data/config/config \
        --target "$SRV_ADDR" \
        --source "`dirname $0`/$1"
}

set -ve
