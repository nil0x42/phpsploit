"""
Set attacker's prefered text editor.

* USE CASES:

# open TARGET setting content with EDITOR:
> set TARGET +

# use `edit` plugin to edit a remote file locally with EDITOR:
> edit /var/www/html/index.php
"""
import os
import sys
import linebuf
import datatypes


type = linebuf.MultiLineBuffer


def setter(value):
    return datatypes.ShellCmd(value)


def default_value():
    raw_value = "vi"
    if "EDITOR" in os.environ:
        raw_value = os.environ["EDITOR"]
    return raw_value
