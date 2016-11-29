"""
Default directory to use for writing
temporary files on attacker machine.

Used as base path for files being edited
with `edit` plugin.
"""
import tempfile

import objects
import datatypes


type = objects.buffers.MultiLineBuffer


def setter(value):
    return datatypes.Path(value, mode="drw")


def default_value():
    return tempfile.gettempdir()
