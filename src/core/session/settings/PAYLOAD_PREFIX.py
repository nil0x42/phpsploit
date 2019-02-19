"""
This variable contains php code which is interpreted
on each http request, just before payload execution.

This setting can be used for example in order to
override a php configuration option with a value
that extends execution scope.

The code will be executed before ANY payload execution.

* Only edit PAYLOAD_PREFIX if you really understand what you're doing
"""
import core
import linebuf
import datatypes


linebuf_type = linebuf.MultiLineBuffer


def validator(value):
    return datatypes.PhpCode(value)


def default_value():
    file_relpath = "data/tunnel/payload_prefix.php"
    file = datatypes.Path(core.BASEDIR, file_relpath)
    return file.read()
