"""PhpSploit base core elements loader.

The most basic PhpSploit elements manager.
It handles user configuration directory, and defines
basic elements such as the following strings:
    basedir -> /path/to/phpsploit/
    coredir -> /path/to/phpsploit/core/
    userdir -> /home/user/.phpsploit/

"""
# directory constants
from src import basedir, coredir
from .config import userdir

# session instance
from .session import session

# tunnel instance
from .tunnel import tunnel

# plugins instance
from .plugins import plugins
