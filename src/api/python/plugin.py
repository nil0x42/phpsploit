import re
from core import plugins


class Plugin:
    """Triggering plugin attributes.

    This object contains attributes from the currently
    running plugin.

    Attributes:

    name
        The plugin name.

    help
        Plugin's docstring (self help message).

    path
        This attribute is the absolute path of the
        plugin's directory.

    category
        Plugin's category.
        It is a formatted version of plugin's parent directory.
        Example:
            >>> plugin = Plugin("plugins/file_system/ls")
            >>> print(plugin.category)
            'File System'

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
