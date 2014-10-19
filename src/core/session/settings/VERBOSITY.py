"""
Bollean variable.

Increases verbosity if is True.
"""
import objects
import datatypes


type = objects.buffers.RandLineBuffer


def setter(value):
    return datatypes.Boolean(value)


def default_value():
    return False
