"""
Default directory to use for writing
temporary files.
"""
import tempfile

import objects
import datatypes


type = objects.buffers.MultiLineBuffer


def setter(value):
    return datatypes.Path(value, mode="drw")


def default_value():
    return tempfile.gettempdir()
