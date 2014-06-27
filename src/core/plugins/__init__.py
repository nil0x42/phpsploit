"""Phpsploit plugins handler

The Plugins() class represents the currently
available plugins.

"""

import os
import re

import core
import objects
from core import session
from datatypes import Path
from decorators import readonly_settings

from .Plugin import Plugin
from .exceptions import BadPlugin


class Plugins(objects.MetaDict):

    def __init__(self):
        """Initalize a plugins list instance"""
        self.blacklist = []
        self.root_dirs = []
        self.root_dirs.append(Path(core.basedir, "plugins", mode='drx'))
        self.root_dirs.append(Path(core.userdir, "plugins", mode='drx'))
        self.current_plugin = None
        super().__init__()

    @readonly_settings("VERBOSITY")
    def reload(self, verbose=False):
        """Reload the plugins list"""
        # if is backed up anyway bo readonly_settings decorator
        if verbose:
            session.Conf.VERBOSITY = True
        self.clear()
        self.errors = 0
        categories = self._load_categories()
        self._load_plugins(categories)
        if self.errors and not session.Conf.VERBOSITY():
            msg = "[-] Plugin loader: %d error(s) found (%s)"
            info = "use `corectl reload-plugins` for more infos"
            print(msg % (self.errors, info))

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
            category_dirs += self._list_path_dirs(root_dir, type="category")

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
                cat_elems = self._list_path_dirs(cat_path, type="plugin")
                for basename, abspath in cat_elems:
                    if basename in (list(self.keys()) + self.blacklist):
                        continue
                    try:
                        self[basename] = Plugin(abspath)
                    except BadPlugin:
                        self.errors += 1

    def _list_path_dirs(self, root_dir, type="plugin"):
        """Returns a list of tuples representing a plugin directory.

        Each tuple is in the form: (basename, abspath)

        Example:
        >>> self._list_path_dirs("/plugins/system")
        [("ls", "/plugins/system/ls"), ("pwd", "/plugins/system/pwd")]

        """
        errmsg = "Bad %s path" % type
        pattern = "^[a-zA-Z0-9_]+$"
        elems = []
        for basename in os.listdir(root_dir):
            try:
                abspath = Path(root_dir, basename, mode='drx')()
            except:
                if not basename.startswith("README"):
                    path = os.path.truepath(root_dir, basename)
                    if os.path.isdir(path):
                        reason = "Permission denied"
                    else:
                        reason = "Not a directory"
                    print("[#] %s: «%s»: %s" % (errmsg, path, reason))
                    self.errors += 1
                continue
            if re.match(pattern, basename):
                elems.append((basename, abspath))
            else:
                reason = "Directory don't match '%s'" % pattern
                print("[#] %s: «%s»: %s" % (errmsg, path, reason))
                self.errors += 1
        return elems


# instanciate plugins list
plugins = Plugins()
