



import re

import objects


class Plugin(objects.MetaDict):
    """Phpsploit plugin class

    This object instanciates a new plugin object.

    Example:
    >>> plugin = Plugin(
    

    """



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
    >>> Env.PLATFORM = "foo"
    >>> Env.PLATFORM = "bar"
    AttributeError: «PLATFORM» variable is read-only
    >>> Env.PLATFORM
    'foo'
    >>> del Env.PLATFORM
    >>> Env.PLATFORM = "bar"
    >>> Env.PLATFORM
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
