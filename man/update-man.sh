#!/bin/bash

set -e
cd $(dirname $0)

man_file="phpsploit.1"
man_txt_file="phpsploit.txt"

txt2tags -q -t man \
    -i man.txt2tags \
    -o "$man_file"
echo "[+] Man page created at: $(readlink -f $man_file)"


MANWIDTH=80 man \
    -P cat "./$man_file" \
    > "$man_txt_file"
echo "[+] Text man page created at: $(readlink -f $man_file)"
