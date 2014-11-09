import re
import copy

import objects


class Environment(objects.VarContainer):
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
    readonly = ["ADDR", "CLIENT_ADDR", "HOST", "HTTP_SOFTWARE",
                "PATH_SEP", "PHP_VERSION", "WEB_ROOT"]
    item_deleters = ["NONE"]

    def __init__(self, value={}, readonly=[]):
        self.readonly += readonly
        self.defaults = {}
        super().__init__(value)
        self.defaults = copy.copy(dict(self))

    def __setitem__(self, name, value):
        if name in self.readonly and name in self.keys():
            raise AttributeError("«{}» variable is read-only".format(name))
        if value == "%%DEFAULT%%":
            if name in self.defaults.keys():
                value = self.defaults[name]
                super().__setitem__(name, value)
            else:
                raise AttributeError("'%s' have no default value" % name)
        else:
            super().__setitem__(name, value)
        if name not in self.defaults.keys():
            self.defaults[name] = self[name]

    def _isattr(self, name):
        return re.match("^[A-Z][A-Z0-9_]+$", name)

    def update(self, dic):
        readonly = self.readonly
        self.readonly = []
        for key, value in dic.items():
            # do not update if the key has been set to
            # another value than the default one.
            if key in self.keys() \
                    and key not in readonly \
                    and self[key] != self.defaults[key]:
                continue
            super().update({key: value})
        self.readonly = readonly

    def clear(self):
        self.defaults = {}
        super().clear()
