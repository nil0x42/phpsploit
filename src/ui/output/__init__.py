"""PhpSploit standard output manager.

This modules handles PhpSploit current outpout, and provides
some informational functions about it, and also the dedicated
stdout wrapper.

Stuff:

* Wrapper(): (file)
    Enable stdout/stdin file wrapping with PhpSploit dedicated
    output file wrappers, providing nice features.

* isatty(): (bool)
    is current output a tty ?

* colors(): (int)
    how many colors current output supports ?

* size(): (tuple)
    return a tuple of terminal's current cols/rows

* columns(): (int)
    return the number of columns current tty have

* lines(): (int)
    return the number of lines current tty have

"""

import os
import sys
import shutil

from . import wrapper

# file wrapper for stdout
Wrapper = wrapper.Stdout

# is output a tty ?
isatty = sys.__stdout__.isatty

# get supported colors from terminal
def colors():
    """Returns the number of colors actually supported by current
    output. Actually, possible values are:
    0   -> for non terminal outputs
    8   -> for windows or standard unix terminals
    256 -> for terminals which 'TERM' env var contains '256'
    """
    if not isatty():
        return 0
    try:
        assert '256' in os.environ['TERM']
        return 256
    except:
        return 8

# get current terminal size
_default_terminal_size = (80, 24)

def size():
    if hasattr(shutil, "get_terminal_size"):
        return tuple(shutil.get_terminal_size(fallback=_default_terminal_size))
    else:
        return _default_terminal_size

columns = lambda: size()[0]
lines = lambda: size()[1]
