"""Common operation on phpsploit target server pathnames.

These functions are designed for use in phpsploit plugins,
for normalizing and extracting server path components.

This module is highly inspired by `os.path` from standard library.
"""
import re
from core import session


_WINPATH_REGEX = re.compile(r"[a-zA-Z]:\\")


def getcwd() -> str:
    """Return the current working directory"""
    return session.Env.PWD


def isabs(path: str) -> bool:
    """Test whether a path is absolute"""
    if path and path[0] in '/\\':
        return True
    if _WINPATH_REGEX.match(path):
        return True
    return False


def abspath(path: str) -> str:
    """Return an absolute path."""
    if not isabs(path):
        sep = '/'
        if '/' not in path and '\\' in path:
            sep = '\\'
        elems = path.split(sep)
        old_path = _split_path(session.Env.PWD)
        path = old_path['root']
        path += old_path['separator'].join(old_path['elems'] + elems)
    return _sanitize_path(path)


def dirname(path: str) -> str:
    """Return the directory component of a pathname"""
    return _split_path(path)['dirname']


def basename(path: str) -> str:
    """Return the final component of a pathname"""
    return _split_path(path)['basename']


def separator(path: str) -> str:
    """Return the path  of a pathname"""
    return _split_path(path)['separator']


def splitdrive(path: str) -> tuple:
    """Split a pathname into drive and path. On Posix, drive is always
    empty."""
    elems = _split_path(path)
    drive = elems['root'][:-1]
    path = path[(len(elems['root']) - 1):]
    return drive, path


# Private function:
def _to_absolute_path(path: str) -> str:
    """Return the absolute version of given path string"""
    if isabs(path):
        return path
    return abspath(path)


# Private function:
def _split_path(path: str) -> dict:
    """Split given path string into path elements"""
    path = _to_absolute_path(path)
    # if linux
    if path.startswith('/'):
        platform = 'nix'
        root = '/'
        sep = '/'
    # if win physical path (C:\)
    elif re.match(_WINPATH_REGEX, path):
        platform = 'win'
        root = path[:3]
        sep = '\\'
    # if win network path (\\1.1.1.1)
    elif path.startswith('\\'):
        platform = 'win'
        root = '\\\\'
        sep = '\\'
        path = root + path.lstrip('\\')
    else:
        raise ValueError("%s: Couldn't parse non-standard path" % path)
    return {"platform": platform,
            "root": root,
            "elems": path[len(root):].split(sep),
            "separator": sep,
            "dirname": sep.join(path.split(sep)[:-1]) + sep,
            "basename": path.split(sep)[-1]}


# Private function:
def _sanitize_path(path):
    """Remove unneeded path elements

    >>> _sanitize_path('/foo/../bar/')
    /bar/
    """
    info = _split_path(path)
    result = []
    elems = info['elems']
    for elem in elems:
        if elem in ['.', '']:
            pass
        elif elem == '..':
            result = result[:-1]
        elif elem == '~':
            info = _split_path(session.Env.HOME)
            result = info['elems']
        else:
            result.append(elem)
    return info['root'] + info['separator'].join(result)
