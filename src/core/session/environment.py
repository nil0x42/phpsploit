import re

import objects


class Environment(objects.MetaDict):
    """Environment Variables

    Instanciate a dict() like object that stores PhpSploit
    environment variables.

    Unlike settings, env vars object works exactly the same way than
    its parent (MetaDict), excepting the fact that some
    items (env vars) are tagged as read-only.
    This behavior only aplies if the concerned variable already
    exists.
    In order to set a tagged variable's value, it must not
    exist already.

    Example:
    >>> Env = Environment()
    >>> Env.HOST = "foo"
    >>> Env.HOST = "bar"
    AttributeError: «HOST» variable is read-only
    >>> Env.HOST
    'foo'
    >>> del Env.HOST
    >>> Env.HOST = "bar"
    >>> Env.HOST
    'bar'

    """
    readonly = ["ADDR", "HOST", "PHP_VERSION", "PATH_SEP",
                "HTTP_SOFTWARE", "WEB_ROOT"]

    def __init__(self, value={}, readonly=[]):
        self.readonly += readonly
        super().__init__(value)

    def __setitem__(self, name, value):
        if name in self.readonly and name in self.keys():
            raise AttributeError("«{}» variable is read-only".format(name))
        super().__setitem__(name, value)

    def _isattr(self, name):
        return re.match("^[A-Z][A-Z0-9_]+$", name)

    def update(self, *args, **kws):
        backup = self.readonly
        self.readonly = []
        super().update(*args, **kws)
        self.readonly = backup
