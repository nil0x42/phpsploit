"""PhpSploit base core elements loader.

The most basic PhpSploit elements manager.
It handles user configuration directory, and defines
basic elements such as the following strings:
    basedir -> /path/to/phpsploit/
    coredir -> /path/to/phpsploit/core/
    userdir -> /home/user/.phpsploit/

"""
### directory constants ###
from src import basedir, coredir
from .config import userdir

### session object ###
from .session import session
