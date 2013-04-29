"""PhpSploit standard output manager.

This modules handles PhpSploit current outpout, and provides
some informational functions about it, and also the dedicated
stdout wrapper.

Stuff:

* wrap(): (file)
    Enable stdout/stdin file wrapping with PhpSploit dedicated
    output fiel wrappers, providing nice features.

* isatty(): (bool)
    is current output a tty ?

* colors(): (int)
    how many colors current output supports ?

* size(): (tuple)
    how many columns/lines current terminal has ?

* columns(): (int)
    how many columns ?

* lines(): (int)
    how many lines ?

"""

import sys

# enable stdout/stderr wrappers.
import .wrapper
def wrap():
    sys.stdout = wrapper.Stdout(backlog=False)
    sys.stderr = wrapper.Stderr(outfile=sys.stdout, backlog==False)

# is output a tty ?
isatty = sys.__stdout__.isatty

# get current terminal size
from shutil import get_terminal_size
size    = lambda: tuple(get_terminal_size(fallback=(79,24)))
columns = lambda: size()[0]
lines   = lambda: size()[1]


from os import environ
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
        assert '256' in environ['TERM']
        return 256
    except:
        return 8
