"""Phpsploit plugins handler

The Plugins() class represents the currently
available plugins.

"""

import os
import re

import core
import objects
from datatypes import Path

from .Plugin import Plugin


class Plugins(objects.MetaDict):

    def __init__(self):
        """Initalize a plugins list instance"""
        self.blacklist = []
        self.root_dirs = []
        self.root_dirs.append(Path(core.basedir, "plugins", mode='drx'))
        self.root_dirs.append(Path(core.userdir, "plugins", mode='drx'))
        self.current_plugin = None
        super().__init__()

    def reload(self):
        """Reload the plugins list"""
        self.clear()
        categories = self._load_categories()
        self._load_plugins(categories)

    def categories(self):
        """Get a list of existing plugin category names"""
        categories = []
        for plugin in self.values():
            categories.append(plugin.category)
        categories.sort()
        return list(set(categories))

    def run(self, argv):
        """Execute the plugin matching given argv list
        """
        # make current_plugin point to self plugin instance
        # this allows api module imports to get triggering
        # plugin attributes.
        plugin = self[argv[0]]
        self.current_plugin = plugin
        try:
            plugin.run(argv)
        finally:
            self.current_plugin = None

    def _load_categories(self):
        """Load currently existing categories.

        The categories are returned in the form of a dictionnary.
        Each element key contains the category name, while value
        if a list of each child plugin absolute path.

        Example:
        >>> self.load_categories()
        {'system': ['/plugins/system/ls', '/plugins/system/pwd'],
         'sql': ['/plugins/sql/mysql', '/plugins/sql/mssql']}

        """
        category_dirs = []
        for root_dir in self.root_dirs:
            category_dirs += self._list_path_dirs(root_dir)

        categories = {}
        for basename, abspath in category_dirs:
            if basename not in categories:
                categories[basename] = []
            categories[basename].append(abspath)
        return categories

    def _load_plugins(self, categories):
        """Fill current plugins instance with currently available plugins.

        All plugins are added to self items, with a key equal to the
        plugin name. Each plugin value is a Plugin() instance.

        """
        for cat_name, cat_paths in categories.items():
            for cat_path in cat_paths:
                cat_elems = self._list_path_dirs(cat_path)
                for basename, abspath in cat_elems:
                    if basename in (list(self.keys()) + self.blacklist):
                        continue
                    self[basename] = Plugin(abspath)

    def _list_path_dirs(self, root_dir):
        """Returns a list of tuples representing a plugin directory.

        Each tuple is in the form: (basename, abspath)

        Example:
        >>> self._list_path_dirs("/plugins/system")
        [("ls", "/plugins/system/ls"), ("pwd", "/plugins/system/pwd")]

        """
        elems = []
        for basename in os.listdir(root_dir):
            try:
                abspath = Path(root_dir, basename, mode='drx')()
            except:
                continue
            if re.match("^[a-zA-Z0-9_]+$", basename):
                elems.append((basename, abspath))
            else:
                print("[-] Ingored plugin path '%s': bad directory name")
        return elems


# instanciate plugins list
plugins = Plugins()
