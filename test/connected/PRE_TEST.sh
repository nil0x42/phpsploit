#!/usr/bin/env bash

# initialize `connected` mode, by starting
# an http server via php development server
# with a phpsploit backdoor into it

. "`dirname $0`/env.inc"

# reset srv_webdir
rm -rf "$SRV_WEBDIR"
mkdir "$SRV_WEBDIR"

./phpsploit \
    --config ./data/config/config \
    --eval 'exploit --get-backdoor' \
    > "$SRV_WEBDIR/index.php"

# STARTING PHPSPLOIT TARGET TEST SERVER
nohup php -S "$SRV_ADDR" -t "$SRV_WEBDIR" > "$SRV_WEBDIR/php.log" 2>&1 &
srv_pid=$!
echo "$srv_pid" > "$SRV_PIDFILE"
