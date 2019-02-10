"""
Default directory to save and load phpsploit session files.

* EXAMPLE:
If SAVEPATH is '/dev/shm', running `session load foo.session`
will implicitly try to load '/dev/shm/foo.session.

This setting also affetcs the `session save` command.
"""
import tempfile

import linebuf
import datatypes


linebuf_type = linebuf.MultiLineBuffer


def validator(value):
    return datatypes.Path(value, mode="drw")


def default_value():
    return tempfile.gettempdir()
