#!/usr/bin/env bash

. "`dirname $0`/env.inc"

srv_pid="`cat $SRV_PIDFILE`"

# KILLING PHPSPLOIT TARGET TEST SERVER
kill $srv_pid
