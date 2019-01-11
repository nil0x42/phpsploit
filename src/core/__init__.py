"""PhpSploit base core elements loader.

The most basic PhpSploit elements manager.
It handles user configuration directory, and defines
basic elements such as the following strings:
    BASEDIR -> /path/to/phpsploit/
    COREDIR -> /path/to/phpsploit/core/
    USERDIR -> /home/user/.phpsploit/
"""
# constant directories
from src import BASEDIR, COREDIR
from .config import USERDIR

# session instance
from .session import session

# tunnel instance
from .tunnel import tunnel

# plugins instance
from .plugins import plugins
