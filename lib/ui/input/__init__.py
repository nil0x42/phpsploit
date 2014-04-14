"""PhpSploit input related classes.

Provides classes related to user input.

SUMMARY:

* Expect()
    Ask a question which expects some user input, with timer feature.

* isatty(): (bool)
    is current input a tty ?

"""

import sys

from .expect import Expect

isatty = sys.stdin.isatty
