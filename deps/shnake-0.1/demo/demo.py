#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ensure that the script is not run with python 2.x
import sys
if (sys.version_info.major < 3):
    exit('shnake library is not compatible with python < 3')

# Make sure the script is not imported
try:
    from __main__ import __file__
except:
    sys.exit('./test.py cannot be imported !')

#### UNIT-TEST ####
import shnake

data = "ls\\\nls\nls"

print(repr(data));

print(shnake.lexer.lex(data))


# import shnake
# parse = shnake.Parser()
#
# if len(sys.argv) > 1:
#     file = open('/tmp/parse.test')
# else:
#     file = None
#
# result = parse(file)
