"""Phpsploit Environment Variables"""

import re
import copy

import metadict
from utils.regex import WORD_TOKEN


class Environment(metadict.VarContainer):
    """Environment Variables

    Instanciate a dict() like object that stores PhpSploit
    environment variables.

    Unlike settings, env vars object works exactly the same way than
    its parent (MarContainer), except that some items (env vars)
    are tagged as read-only.
    * This behavior only aplies if the concerned variable already exists.
    * To set a tagged variable's value, it must not exist.

    Example:
    >>> Env = Environment()
    >>> Env.HOST = "foo"
    >>> Env.HOST = "bar"
    AttributeError: «HOST» variable is read-only
    >>> Env.HOST
    foo
    >>> del Env.HOST
    >>> Env.HOST = "bar"
    >>> Env.HOST
    bar
    """
    readonly = ["ADDR", "CLIENT_ADDR", "HOST", "HTTP_SOFTWARE",
                "PATH_SEP", "PHP_VERSION", "WEB_ROOT"]
    item_deleters = ["NONE"]

    def __init__(self, value=None, readonly=None):
        if value is None:
            value = {}
        if readonly is None:
            readonly = []

        self.readonly += readonly
        self.defaults = {}
        super().__init__(value)
        self.defaults = copy.copy(dict(self))

    def __setitem__(self, name, value):
        # ensure the env var name has good syntax
        if name == "__DEFAULTS__":
            raise KeyError("illegal name: %r" % name)
        if not WORD_TOKEN.fullmatch(name):
            raise KeyError("illegal name: %r doesn't match %s"
                           % (name, WORD_TOKEN.pattern))
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

    @staticmethod
    def _isattr(name):
        return re.match("^[A-Z][A-Z0-9_]+$", name)

    def update(self, new_dict):
        readonly = self.readonly
        self.readonly = []
        if "__DEFAULTS__" in new_dict.keys():
            self.defaults = copy.copy(dict(new_dict.pop("__DEFAULTS__")))
        elif hasattr(new_dict, "defaults"):
            self.defaults = copy.copy(dict(new_dict.defaults))
        for key, value in new_dict.items():
            # do not update if the key has been set to
            # another value than the default one.
            if key in self.keys() \
                    and key not in readonly \
                    and key in self.defaults.keys() \
                    and self[key] != self.defaults[key]:
                continue
            super().update({key: value})
        self.readonly = readonly

    def clear(self):
        self.defaults = {}
        super().clear()

    def signature(self):
        """returns remote server signature hash for comparison
        """
        signature = ()
        for var in ["ADDR", "HTTP_SOFTWARE", "PATH_SEP", "PLATFORM", "USER"]:
            if var in self.keys():
                signature += (self[var],)
        return hash(signature)
