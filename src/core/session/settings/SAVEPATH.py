"""
The default directory to use for saving and
loading phpsploit sessions.

For example, if $SAVEPATH is '/dev/shm', running
`session load foo.session` will implicitly try to get
the session file '/dev/shm/foo.session.
This feature also works with the `session save` command.
"""
import tempfile

import objects
import datatypes


type = objects.buffers.MultiLineBuffer


def setter(value):
    return datatypes.Path(value, mode="drw")


def default_value():
    return tempfile.gettempdir()
