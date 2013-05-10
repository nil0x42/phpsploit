"""PhpSploit base core elements loader.

The most basic PhpSploit elements manager.
It handles user configuration directory, and defines
basic elements such as the following strings:
    basedir -> /path/to/phpsploit/
    coredir -> /path/to/phpsploit/core/
    userdir -> /home/user/.phpsploit/

"""
# get basedir and coredir from lib package
from lib import basedir, coredir

# determine user directory
from .config import userdir

del config
