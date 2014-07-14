"""Common operation on phpsploit target server pathnames.

These functions are designed for use in phpsploit plugins,
for normalizing and extracting server path components.

This module is mostly inspired by the `os.path` standard
python submodule.
"""


import re

from core import session


_windows_path_matcher = '[a-zA-Z]:\\\\'


def isabs(path):
    """Test whether a path is absolute"""
    if path.startswith('/') or path.startswith('\\'):
        return True
    elif re.match(_windows_path_matcher, path):
        return True
    else:
        return False


def abspath(path):
    """Return an absolute path."""
    if not isabs(path):
        slash = '/'
        if '/' not in path and '\\' in path:
            slash = '\\'
        elems = path.split(slash)
        oldPath = _split_path(session.Env.PWD)
        path = oldPath['root']
        path += oldPath['slash'].join(oldPath['elems'] + elems)
    return _sanitize_path(path)


def dirname(path):
    """Return the directory component of a pathname"""
    return _split_path(path)['dirname']


def basename(path):
    """Return the final component of a pathname"""
    return _split_path(path)['basename']


def splitdrive(path):
    """Split a pathname into drive and path. On Posix, drive is always
    empty."""
    elems = _split_path(path)
    drive = elems['root'][:-1]
    path = path[(len(elems['root']) - 1):]
    return drive, path


# Private function:
# Return the absolute version of given path string.
def _to_absolute_path(path):
    if isabs(path):
        return path
    return abspath(path)


# Private function:
# Split the given path string into a dict of path elements.
def _split_path(path):
    path = _to_absolute_path(path)
    # if linux
    if path.startswith('/'):
        platform = 'nix'
        root = '/'
        slash = '/'
    # if win physical path (C:\)
    elif re.match(_windows_path_matcher, path):
        platform = 'win'
        root = path[:3]
        slash = '\\'
    # if win network path (\\1.1.1.1)
    elif path.startswith('\\'):
        platform = 'win'
        root = '\\\\'
        slash = '\\'
        path = root + path.lstrip('\\')
    else:
        raise ValueError("%s: Could not parse non-standard path" % path)
    dirname = slash.join(path.split(slash)[:-1]) + slash
    basename = path.split(slash)[-1]
    elems = path[len(root):].split(slash)
    result = {'platform': platform,
              'root': root,
              'elems': elems,
              'slash': slash,
              'dirname': dirname,
              'basename': basename}
    return result


# Private function:
# Remove unneeded path elements.
#   - example: '/foo/../bar/' becomes '/bar/'
def _sanitize_path(path):
    info = _split_path(path)
    result = []
    elems = info['elems']
    for x in elems:
        if x in ['.', '']:
            pass
        elif x == '..':
            result = result[:-1]
        elif x == '~':
            info = _split_path(session.Env.HOME)
            result = info['elems']
        else:
            result.append(x)
    return info['root'] + info['slash'].join(result)
