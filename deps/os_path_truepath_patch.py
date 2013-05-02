"""Patch os.path standard library to add to it the tryepath() function,
that supports multiple path arguments, and automatically joins them
with user dir and env vars expanded. The final result path is then
normalized with os.path.realpath()

"""
import os.path

def _truepath(*elems):
    """A fusion of join(), expandvars(), expanduser() and realpath()"""
    expand = lambda s: os.path.expandvars(os.path.expanduser(s))
    elems = (expand(s) for s in elems)
    path = os.path.join(*elems)
    return os.path.realpath(path)

os.path.truepath = _truepath
