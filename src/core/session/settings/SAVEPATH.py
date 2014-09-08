"""
The default directory to use for saving and
loading phpsploit sessions when a filename
if given instead of a file path.
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
