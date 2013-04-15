"""PhpSploit Session Manager

When imorted for the first time, the "session" package initializes it
self as a PhpSploit blank session, with its default values.

"""
import .settings, .environment
Conf = settings.Init()
Env  = environment.Init()

from .pickle import load, dump



"""BEHAVIOR SIMULATION

>>> import session


Setter:
>>> session.Conf.REQ_INTERVAL = "1-5"
>>> setattr(session.Conf, 'REQ_INTERVAL', "1-5")
>>> session.Conf('REQ_INTERVAL', "1-5")

Getter:
>>> session.Conf.REQ_INTERVAL
(1.0, 5.0)
>>> getattr(session.Conf, 'REQ_INTERVAL')
(1.0, 5.0)
>>> session.Conf('REQ_INTERVAL')
(1.0, 5.0)

Checker:
>>> hasattr(session.Conf, 'REQ_INTERVAL')
True
>>> session.Conf('REQ_INTERVAL') is not NotImplemented
True

Deleter:
>>> del session.Conf.REQ_INTERVAL
>>> delattr(session.Conf, 'REQ_INTERVAL')

Caller: # return the dynamic value (Interval types return float between tuple)
>>> session.Conf.REQ_INTERVAL()
3.2
>>> getattr(session.Conf, 'REQ_INTERVAL')()
4.9
>>> session.Conf('REQ_INTERVAL')()
2.1

Nice repr: # return a nice, human readable var type representation
>>> session.Conf.REQ_INTERVAL.repr


self.CNF['ENV']['CWD']
session.Environment.CWD



self.CNF['ENV']['CWD']
session.Env.CWD
session.Conf.CWD
session.Alias.CWD

session.Environment.CWD
session.Settings.CWD
session.Aliases.CWD

session.Server.HOME

"""
