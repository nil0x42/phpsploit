"""
The web URI to use as remote target.
In order to run a remote exploitation session
the given URL should be backdoored.

NOTE: The backdoor to use can be retrieved by
      running `exploit --get-backdoor` command.
"""
import objects
import datatypes


type = objects.buffers.RandLineBuffer


def setter(value):
    if str(value).lower() in ["", "none"]:
        return default_value()
    else:
        return datatypes.Url(value)


def default_value():
    return None
