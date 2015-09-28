"""A small os.path module improvement.

Add a truepath() function, which supports multipl path arguments,
and automatically joins them with user dir and env vars expanded.

The final result path is then normalized with os.path.realpath()

Author: nil0x42
"""

import os

def truepath(*elems):
    """A fusion of join(), expandvars(), expanduser() and realpath()"""
    expand = lambda s: os.path.expandvars(os.path.expanduser(s))
    elems = (expand(s) for s in elems)
    path = os.path.join(*elems)
    return os.path.realpath(path)
