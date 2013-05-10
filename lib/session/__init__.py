"""PhpSploit Session Manager

When imorted for the first time, the "session" package initializes it
self as a PhpSploit blank session, with its default values.

"""
from . import settings, environment, aliases

Conf  = settings.Settings()       # settings `session.Conf`
Env   = environment.Environment() # env vars `session.Env`
Alias = aliases.Aliases()         # aliases  `session.Alias`




#Alias = aliases.
#Env = environment.New()


"""

>>> from session import session
>>> session.update('/tmp/phpsploit.session')
>>> session(


>>> import session
>>> session.load(


>>> import session
>>> session.load('/tmp/phpsploit.session') # return new sess object
>>> session != session('/tmp/new-session.txt')
>>> session.update('/tmp/new-session.txt')
>>> session.diff('/tmp/file') # get session diff





>>>


"""
