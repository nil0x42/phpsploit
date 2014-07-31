#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

# Ensure that the script is not run with python 2.x
if (sys.version_info.major < 3):
    sys.exit('shnake library is not compatible with python < 3')

# Ensure the script is not imported
try:
    from __main__ import __file__
    del __file__
except:
    sys.exit('./demo.py cannot be imported !')

# TEST
import shnake

# lexer behavior
single_line_cmd = "ls -la /tmp 2>&1 && echo foo'bar'\ "
print("DEMO: shnake.lex()")
print("The shnake lexer handles single line commands:")
print()
print("Raw command:   %r" % single_line_cmd)
result = shnake.lex(single_line_cmd)
print("Lexed command: %r" % result)
print()
print()

# parser behavior
multi_line_cmd = "cmd1-part1\\\ncmd1-part2\ncmd2"
print()
print("DEMO: shnake.parse()")
print("The shnake parser is a wrapper for the lexer.")
print("Its handles multi-line strings, so it can parse file buffers")
print()
print("Raw command:    %r" % multi_line_cmd)
result = shnake.parse(multi_line_cmd)
print("Parsed command: %r" % result)
print()
print()

# command interpreter demo
print("DEMO: shnake.Shell()")
print("This shnake shell is a command line interpreter.")
print("Type: `help` in the shell interface")
interpreter = shnake.Shell()
interpreter.prompt = "shnake > "
interpreter.cmdloop()
