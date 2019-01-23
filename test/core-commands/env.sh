#!/usr/bin/env bash

$PHPSPLOIT -e 'exploit; env' > $TMPFILE

# check output contents
< $TMPFILE grep -q '^Environment Variables$'
< $TMPFILE grep -q '^=====================$'
< $TMPFILE grep -q '^    Variable          Value$'
< $TMPFILE grep -q '^    --------          -----$'
< $TMPFILE grep -q '^    ADDR              '
< $TMPFILE grep -q '^    CLIENT_ADDR       '
< $TMPFILE grep -q '^    HOME              '
< $TMPFILE grep -q '^    HOST              '
< $TMPFILE grep -q '^    HTTP_SOFTWARE     '
< $TMPFILE grep -q '^    PATH_SEP          '
< $TMPFILE grep -q '^    PHP_VERSION       '
< $TMPFILE grep -q '^    PLATFORM          '
< $TMPFILE grep -q '^    PORT              '
< $TMPFILE grep -q '^    PWD               '
< $TMPFILE grep -q '^    USER              '
< $TMPFILE grep -q '^    WEB_ROOT          '
< $TMPFILE grep -q '^    WRITEABLE_TMPDIR  '
< $TMPFILE grep -q '^    WRITEABLE_WEBDIR  '
