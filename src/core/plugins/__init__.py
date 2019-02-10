"""Phpsploit plugins handler
"""

import os
import re

import ui
import metadict
import core
from core import session
from datatypes import Path
from decorators.readonly_settings import readonly_settings
import utils.path

from .Plugin import Plugin
from .exceptions import BadPlugin

DEFAULT_PLUGIN = Plugin(core.BASEDIR +
                        "data/plugin-sample/category_name/plugin_example")


class Plugins(metadict.MetaDict):
    """Phpsploit plugins handler

    The Plugins() class represents the currently
    available plugins.

    """

    def __init__(self):
        """Initalize a plugins list instance"""
        self.blacklist = []
        self.root_dirs = []
        self.root_dirs.append(Path(core.BASEDIR, "plugins", mode='drx'))
        self.root_dirs.append(Path(core.USERDIR, "plugins", mode='drx'))
        self.current_plugin = DEFAULT_PLUGIN
        super().__init__()

    @readonly_settings("VERBOSITY")
    def reload(self, verbose=False):
        """Reload the plugins list"""
        if verbose:
            session.Conf.VERBOSITY = True
        self.clear()
        categories = self._load_categories()
        errors = self._load_plugins(categories)
        if errors > 0 and ui.interface.interactive:
            msg = "[#] Plugin loader: %d error(s) found"
            if not verbose:
                msg += " (use `corectl reload-plugins` for more infos)"
            session.Conf.VERBOSITY = True
            print(msg % errors)

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
        plugin.argv = argv
        self.current_plugin = plugin
        try:
            return plugin.run(argv)
        finally:
            self.current_plugin = DEFAULT_PLUGIN

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

        Some plugins may fail to load, so numer of load errors is returned
        """
        errors = 0
        for cat_name, cat_paths in categories.items():
            for cat_path in cat_paths:
                cat_elems = self._list_path_dirs(cat_path, type="plugin")
                for basename, abspath in cat_elems:
                    if basename in list(self.keys()) + self.blacklist:
                        continue
                    try:
                        self[basename] = Plugin(abspath)
                    except BadPlugin:
                        errors += 1
        return errors

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
            path = utils.path.truepath(root_dir, basename)
            try:
                abspath = Path(root_dir, basename, mode='drx')()
            except:
                if not basename.startswith("README"):
                    if os.path.isdir(path):
                        reason = "Permission denied"
                    else:
                        reason = "Not a directory"
                    print("[#] %s: «%s»: %s" % (errmsg, path, reason))
                    self.errors += 1
                continue
            if re.match(pattern, basename):
                elems.append((basename, abspath))
            elif basename.endswith(".DISABLED"):
                continue
            else:
                reason = "Directory don't match '%s'" % pattern
                print("[#] %s: «%s»: %s" % (errmsg, path, reason))
                self.errors += 1
        return elems


# instanciate plugins list
plugins = Plugins()
