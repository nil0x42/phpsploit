"""
Enable or Disable phpsploit framework verbosity.
"""
import linebuf
import datatypes


type = linebuf.RandLineBuffer


def setter(value):
    return datatypes.Boolean(value)


def default_value():
    return False
