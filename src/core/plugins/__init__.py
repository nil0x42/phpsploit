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
    valid_plugin_name = re.compile("^[a-zA-Z0-9_-]+$")

    def __init__(self):
        """Initalize a plugins list instance"""
        self.errors = 0
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
        self.errors = 0
        categories = self._load_categories()
        num_loaded = self._load_plugins(categories)
        if self.errors:
            msg = "[#] %d errors encountered while loading plugins"
            if not verbose:
                msg += " (use `corectl reload-plugins` for + infos)"
            session.Conf.VERBOSITY = True
            print(msg % self.errors)
        if verbose or self.errors or ui.input.isatty():
            if num_loaded:
                print("[*] %d plugins correctly loaded" % num_loaded)
            else:
                print("[-] No plugins were loaded")
        return not self.errors

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
            return plugin.run(argv)
        finally:
            self.current_plugin = DEFAULT_PLUGIN

    def _log_error(self, path, errmsg, _type="plugin"):
        print("[#] Couldn't load %s: «%s»" % (_type, path))
        print("[#]     " + errmsg)
        print("[#] ")
        self.errors += 1

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
            category_dirs += self._list_path_dirs(root_dir, _type="category")

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
        num_loaded = 0
        for cat_paths in categories.values():
            for cat_path in cat_paths:
                cat_elems = self._list_path_dirs(cat_path, _type="plugin")
                for name, path in cat_elems:
                    if name in self.keys():
                        msg = "Name already taken by %r" % self[name].path
                        self._log_error(path, msg)
                    elif name in self.blacklist:
                        msg = "Name already taken by `%s` command" % name
                        self._log_error(path, msg)
                    try:
                        self[name] = Plugin(path)
                    except BadPlugin:
                        self.errors += 1
                    else:
                        num_loaded += 1
        return num_loaded

    def _list_path_dirs(self, root_dir, _type="plugin"):
        """Returns a list of tuples representing a plugin directory.

        Each tuple is in the form: (basename, abspath)

        Example:
        >>> self._list_path_dirs("/plugins/system")
        [("ls", "/plugins/system/ls"), ("pwd", "/plugins/system/pwd")]

        """
        elems = []
        for basename in os.listdir(root_dir):
            path = utils.path.truepath(root_dir, basename)
            if not os.path.isdir(path):
                self._log_error(path, "Not a directory", _type)
            elif not os.access(path, os.X_OK | os.R_OK):
                self._log_error(path, "Permission denied", _type)
            elif not self.valid_plugin_name.match(basename):
                msg = ("Folder name doesn't match " +
                       repr(self.valid_plugin_name.pattern))
                self._log_error(path, msg, _type)
            else:
                elems.append((basename, path))
        return elems


# instanciate plugins list
plugins = Plugins()
