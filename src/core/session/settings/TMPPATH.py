"""
Default phpsploit temporary directory.

* USE CASES:
Used as base path for files edited with `edit` plugin.
"""
import tempfile

import linebuf
import datatypes


type = linebuf.MultiLineBuffer


def setter(value):
    return datatypes.Path(value, mode="drw")


def default_value():
    return tempfile.gettempdir()
