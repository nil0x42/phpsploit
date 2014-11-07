"""
This variable contains php code which is interpreted
on each http request, just before payload execution.

This setting can be used for example in order to
override a php configuration option with a value
that extends execution scope, or aniything you want
to be executed anytime.

NOTE: If you do not understand what you're doing,
      keep this setting with default value.
"""
import core
import objects
import datatypes


type = objects.buffers.MultiLineBuffer


def setter(value):
    return datatypes.PhpCode(value)


def default_value():
    file_relpath = "data/tunnel/payload_prefix.php"
    file = datatypes.Path(core.basedir, file_relpath)
    return file.read()
