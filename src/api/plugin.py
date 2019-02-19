"""Provide access to attributes of currently running plugin"""
__all__ = ["plugin"]

import re
from core import plugins


class Plugin:
    """Get access to currently running plugin attributes.

    Usage:
    >>> from api import plugin

    Attributes:

    * name (type: str)
        # Plugin name.
        >>> plugin.name
        'foobar'

    * help (type: str)
        # Plugin docstring (detailed help).
        >>> print(plugin.help)
        [*] foobar: An imaginary phpsploit plugin
        DESCRIPTION:
            An imaginary foobar plugin description.
        ...

    * path (type: str)
        # Absolute path of plugin's root directory.
        >>> plugin.path
        '/home/user/phpsploit/plugins/parent_dir/foobar/'

    * category (type: str)
        # Plugin's category name (parent directory).
        >>> plugin.category
        'Parent Dir'
    """

    def __init__(self):
        pass

    def __getattr__(self, attr):
        errmsg = "type object '%s' has no attribute '%s'"
        if attr in dir(self):
            return getattr(plugins.current_plugin, attr)
        raise AttributeError(errmsg % (self.__class__.__name__, str(attr)))

    def __dir__(self):
        result = []
        for attr in dir(plugins.current_plugin):
            obj = getattr(plugins.current_plugin, attr)
            if re.match("^[a-z]+$", attr) and not callable(obj):
                result.append(attr)
        return result


# instanciate plugin object (for use within python API)
plugin = Plugin()
