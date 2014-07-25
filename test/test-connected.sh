#!/usr/bin/env bash


srv_addr="127.0.0.1:`shuf -i 10000-65500 -n 1`"
srv_webdir="/tmp/`uuidgen`/"

mkdir -p "$srv_webdir"
echo `phpsploit -e 'exploit --get-backdoor'` > "$srv_webdir/index.php"

srv_cmdline="php -S $srv_addr -t $srv_webdir"

$srv_cmdline &> "$srv_webdir/php.log" &

phpsploit \
    --target "$srv_addr" \
    --eval "exploit; cd $srv_webdir; env" \
    --interactive

kill `ps -ef | grep "$srv_cmdline" | head -n 1 | awk '{print $2}'` && \
/bin/rm -rf "$srv_webdir" && \
echo "INFO: quick php server correctly terminated" || \
echo "WARNING: quick php server could not be terminated correctly !"
