"""PhpSploit Session Manager

When imorted for the first time, the "session" package initializes it
self as a PhpSploit blank session, with its default values.

>>> import session
>>> session.load('/tmp/phpsploit.session') # return new sess object
>>> session != session('/tmp/new-session.txt')
>>> session.update('/tmp/new-session.txt')
>>> session.diff('/tmp/file') # get session diff

"""
import re
#import .baseclass, .settings
from . import baseclass
from . import settings


class Session(baseclass.MetaDict):
    """Phpsploit Session

    """

    def __init__(self):
        """Instanciate the phpsploit session, it handles configuration
        settings, environment variables, command aliases, http response
        cache and readline history (if readline is available).

        """
        super().__init__()

        self.Conf = settings.Settings()
        self.Env = baseclass.MetaDict(title="Environment Variables")
        self.Alias = baseclass.MetaDict(title="Command Aliases")


    def _isattr(self, name):
        """Session items are alphabetic and capitalized strings"""
        return re.match("^[A-Z][a-z]+$", name)

session = Session()
