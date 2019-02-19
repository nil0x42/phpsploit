"""Phpsploit framework core loader.

This pseudo module is designed to be imported (import lib) from
the phpsploit script launcher (./phpsploit).
It also can be imported from phpsploit root directory through a
python interpreter for debugging purposes.

It loads the phpsploit core, spreading required dependencies
(./deps directory) then overwriting sys.path's first element to
the current directory (./lib/), making all self contained elements
directly importable from python.

"""
import os
import sys

# load phpsploit dependencies before anything else
import deps

from . import utils

BASEDIR = utils.path.truepath(sys.path[0]) + os.sep
COREDIR = os.path.join(BASEDIR, __name__) + os.sep

# use current directory as main python path
sys.path[0] = COREDIR

del deps, sys, os  # clean package's content
