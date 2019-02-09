"""
Enable or Disable phpsploit framework verbosity.
"""
import objects
import datatypes


type = objects.linebuf.RandLineBuffer


def setter(value):
    return datatypes.Boolean(value)


def default_value():
    return False
