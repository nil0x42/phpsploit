#!/usr/bin/env bash

# This script eases some debugging tasks.
# It runs a php server, writes a backdoor to it,
# then it runs the phpsploit framework with this
# backdoor.
# It means that running this script runs a
# phpsploit session that is connected to a backdoor.
# When leaving the framework, the php server is killed,
# and its root directory removed.

srv_addr="127.0.0.1:`shuf -i 10000-65500 -n 1`"
srv_webdir="/tmp/`uuidgen`/"

mkdir -p "$srv_webdir"
echo `./phpsploit -e 'exploit --get-backdoor'` > "$srv_webdir/index.php"

php -S "$srv_addr" -t "$srv_webdir" &> "$srv_webdir/php.log" &
srv_pid=$!

./phpsploit \
    --target "$srv_addr" \
    --eval "exploit; cd \"$srv_webdir\"; env" \
    --interactive

kill $srv_pid && /bin/rm -rf "$srv_webdir" && \
echo "[+] php server correctly terminated" || \
echo "[!] could not kill php server ($srv_pid)"
