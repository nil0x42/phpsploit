"""File path handling

The functions described here provide some aditional features
unavailable in the os.path standard module.

Author: nil0x42
"""

import os


def truepath(*elems):
    """Joins the given path(s), expanding environment variables
    and user directory ('~').
    """
    expand = lambda s: os.path.expandvars(os.path.expanduser(s))
    elems = (expand(s) for s in elems)
    path = os.path.join(*elems)
    return os.path.realpath(path)
