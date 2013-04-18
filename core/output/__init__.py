"""PhpSploit standard output manager.

This module handles any standard output related features for the
PhpSploit framework. It provides terminal color features, gives
informations about the current output (tty or non-interactive pipe),
provides the stdout Wrapper with backlogging capability, and tells
how many colors the current output terminal (if any), actually
supports.

"""
from .stdout import Wrapper

from .color import colorize, decolorize, colors

from sys import __stdout__
isatty = __stdout__.isatty


