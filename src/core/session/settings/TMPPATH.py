"""
Default directory to use for writing
temporary files.
"""
import tempfile

import objects
import datatypes


type = objects.settings.RandLineBuffer


def setter(value):
    return datatypes.Path(value, mode="drw")


def default_value():
    raw_value = tempfile.gettempdir()
    return setter(raw_value)
