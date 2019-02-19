"""PhpSploit User Input (STDIN) Handler

This package provides UI features relaed to Standard Input
"""
__all__ = ["Expect", "isatty"]

import sys
from .expect import Expect


def isatty() -> bool:
    """Return whether input is an 'interactive' stream.

    Return False if it can't be determined.
    """
    return sys.__stdin__.isatty()
