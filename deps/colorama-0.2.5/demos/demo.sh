#!/usr/bin/env bash

# Script to demonstrate features of colorama.

# This demo is also used to verify correctness visually, because we don't have automated tests.

# Implemented as a bash script which invokes python so that we can test the
# behaviour on exit, which resets default colors again.

python demo01.py

python demo02.py

python demo03.py

rm -f demo04.out
python demo04.py 2> demo04.out
cat demo04.out

python demo05.py

python demo06.py

