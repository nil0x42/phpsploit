"""A decorator for limiting session settings scope.

The readonly_settings decorator takes an undefined number of
string arguments, representing the names of the settings
to backup, in order to force them to be kept back after
function execution.

If no arguments are set, then all session settings will
be write protected.

Example:
    >>> @readonly_settings("SAVEPATH")
    >>> def test_function():
    ...     session.Conf.SAVEPATH = "/modified/savepath"
    ...     session.Conf.TMPPATH = "/modified/tmppath"
    ...     # calling a function that makes use of the altered
    ...     # session settings.
    ...     session.dump(None)
    ...     return None
    ...
    >>> session.Conf.SAVEPATH = "/default/savepath"
    >>> session.Conf.TMPPATH = "/default/tmppath"
    >>>
    >>> print(session.CONF.SAVEPATH)
    "/default/savepath"
    >>> print(session.CONF.TMPPATH)
    "/default/tmppath"
    >>>
    >>> test_function()
    >>>
    >>> print(session.CONF.SAVEPATH)
    "/default/savepath"
    >>> print(session.CONF.TMPPATH)
    "/modified/tmppath"

As you can see in the example above, SAVEPATH have been
write protected, and it has been reset to it's old state
after function execution.

"""
from core import session


def readonly_settings(*decorator_args):
    # no args = all settings
    if not decorator_args:
        decorator_args = list(session.Conf.keys())

    def decorator(function):
        def wrapper(*args, **kwargs):
            # backup all protected settings
            protected_settings = {}
            for name in decorator_args:
                protected_settings[name] = session.Conf[name]
            # execute decorated function
            try:
                retval = function(*args, **kwargs)
            # restore protected settings
            finally:
                for name, value in protected_settings.items():
                    session.Conf[name] = value
            return retval

        return wrapper

    return decorator
