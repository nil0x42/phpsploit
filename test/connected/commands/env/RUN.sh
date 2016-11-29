#!/usr/bin/env bash

. "`dirname $0`/../../env.inc"

# check return value of phpsploit `env` command
run_phpsploit_test 'output.src' &> /dev/null

output="`run_phpsploit_test 'output.src' | sed -e '1,/^running PHP /d'`"

# display output
echo "$output"

# check output contents
echo "$output" | grep -q '^Environment Variables$'
echo "$output" | grep -q '^=====================$'
echo "$output" | grep -q '^    Variable          Value$'
echo "$output" | grep -q '^    --------          -----$'
echo "$output" | grep -q '^    ADDR              '
echo "$output" | grep -q '^    CLIENT_ADDR       '
echo "$output" | grep -q '^    HOME              '
echo "$output" | grep -q '^    HOST              '
echo "$output" | grep -q '^    HTTP_SOFTWARE     '
echo "$output" | grep -q '^    PATH_SEP          '
echo "$output" | grep -q '^    PHP_VERSION       '
echo "$output" | grep -q '^    PLATFORM          '
echo "$output" | grep -q '^    PORT              '
echo "$output" | grep -q '^    PWD               '
echo "$output" | grep -q '^    USER              '
echo "$output" | grep -q '^    WEB_ROOT          '
echo "$output" | grep -q '^    WRITEABLE_TMPDIR  '
echo "$output" | grep -q '^    WRITEABLE_WEBDIR  '

# check length
[ "`echo "$output" | wc -l`" -eq 20 ]
