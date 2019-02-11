"""PhpSploit User Output (STDOUT) Handler

This package provides UI features relaed to Standard Output
"""
__all__ = ["Wrapper", "isatty", "colors", "size", "columns", "lines"]

import os
import sys
import shutil

from .wrapper import Stdout as Wrapper


def isatty() -> bool:
    """True if STDOUT is connected to a tty device."""
    return sys.__stdout__.isatty()


def colors() -> int:
    """Returns the number of colors actually supported by current
    output. Actually, possible values are:
    0   -> for non terminal outputs
    8   -> for windows or standard unix terminals
    256 -> for terminals which 'TERM' env var contains '256'
    """
    if not isatty():
        return 0
    if "TERM" in os.environ and "256" in os.environ["TERM"]:
        return 256
    return 8


def size(fallback=(80, 24)) -> tuple:
    """Get the size of the terminal window."""
    return tuple(shutil.get_terminal_size(fallback=fallback))


def columns() -> int:
    """Get the number of columns of the terminal window."""
    return size()[0]


def lines() -> int:
    """Get the number of lines of the terminal window."""
    return size()[1]
