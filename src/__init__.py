"""Phpsploit framework core loader.

This pseudo module is designed to be imported (import lib) from
the phpsploit script launcher (./phpsploit).
It also can be imported from phpsploit root directory through a
python interpreter for debugging purposes.

It loads the phpsploit core & overwrites sys.path's first element to
the current directory (./lib/), making all self contained elements
directly importable from python.

"""
import os
import sys

from . import utils

BASEDIR = utils.path.truepath(sys.path[0]) + os.sep
COREDIR = os.path.join(BASEDIR, __name__) + os.sep

# use current directory as main python path
sys.path[0] = COREDIR

# add src/core/shnake-0.5/ to python path
shnake_path = os.path.join(COREDIR, "shnake-0.5") + os.sep
sys.path.insert(0, shnake_path)

del sys, os, shnake_path  # clean package's content
