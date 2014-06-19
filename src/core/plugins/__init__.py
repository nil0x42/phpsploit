"""Phpsploit plugins handler

The Plugins() class represents the currently
available plugins.

"""

import os

from datatypes import Path


class Plugins:

    def __init__(self):
        self.blacklist = []
        self.path_list = []
        self.path_list.append(Path(core.basedir, "plugins", mode='dx'))
        self.path_list.append(Path(core.userdir, "plugins", mode='dx'))

    def update(self):
        """update the plugins list
        """
        categories = self.get_categories()
        self.items = self.get_plugins(categories)

    def blacklist(self, lst):
        """make a name list unusable as plugins
        """
        self.blacklist += lst

    def commands(self):
        """returns the list of plugin commands
        """
        return self.items.keys()

    def categories(self):
        """returns the list of plugin categories
        """
        categories = list()
        for item in self.items.values():
            categories.append(item['category'])
        categories.sort()
        return list(set(categories))

    def list_category(self, category):
        """provides the list of any plugin
        that belong to the given category
        """
        items = list()
        for name, item in self.items.items():
            if item['category'] == category:
                items.append(name)
        items.sort
        return items

    def get(self, name, item=None):
        """returns the value of the plugin's item
        """
        if item is None:
            return self.items[name]

        return self.items[name][item]

    def get_plugins(self, categories):
        """return a dictionnary of plugins, each one containing
        the following elements:
        - category: the plugin's category
        - path:     the plugin's root directory
        - script:   the plugin script as string
        - help:     the plugin's docstring
        """
        plugins = dict()

        for cat_name, cat_paths in categories:
            for cat_path in cat_paths:
                cat_elems = self.get_path_elems(cat_path)
                for name, path in cat_elems:
                    if name not in plugins and name not in self.blacklist:
                        elem = self.load_plugin(name, path)
                        if elem:
                            elem['category'] = cat_name
                            elem['path']     = path.name
                            plugins[name] = elem
        return plugins

    def load_plugin(self, name, path):
        """load the given plugin "name" at "path".
        The return is False if the given arguments do not match a valid
        PhpSploit plugin. Otherwise, a dictionnary containg the "help"
        and "script" strings is returned.
        """
        def load_error(reason):
            print("[-] Couldn't load «%s» plugin: %s" % (name, reason))
            return False

        if not path.isdir():
            return False

        plugin = dict()
        # try to get the plugin script
        try:
            plugin['script'] = Path(
            plugin['script'] = getpath(path.name, "plugin.py").read().strip()
        except:
            return load_error("not found")
        # check if the script has some content
        if not plugin['script']:
            return load_error("is empty")
        # load the plugin script's help (docstring)
        plugin['help'] = ""
        try:
            scriptCode = compile(plugin['script'], "", "exec")
        except ValueError as e:
            return load_error(e.message)
        # use plugin's docstring as help string (if any)
        if "__doc__" in scriptCode.co_names:
            plugin['help'] = scriptCode.co_consts[0]

        return plugin


    def get_categories(self):
        """get the plugin available categories, browsing the plugins dir"""
        categories = dict()

        paths = list()
        for root in self.path_list:
            paths+= self.get_path_elems(root)

        for name, path in paths:
            if not name in categories:
                categories[name] = list()
            categories[name].append(path)
        return(categories.items())


    def get_path_elems(self, root):
        result = list()
        for name in os.listdir(root.name):
            path = getpath(root.name, name)
            if os.path.isdir(path.name):
                if self.bad_string(name):
                    msg = 'Ignored plugin path %s: invalid directory name'
                    print P_err+msg % quot(path.name)
                else:
                    result.append((name, path))
        return(result)


    def bad_string(self, string):
        for char in string:
            if char not in P_CHARS:
                return(True)
        return(False)




class Run:
    libs_path = getpath('core/pspapi').name

    def __init__(_self, argv, plugins, core):
        """ in this class, we use _self instead of self,
        because the self object is used for the plugins API

        """
        # instantiate the plugin's self vars
        cmd = dict()
        cmd['name'] = argv[0]
        cmd['argv'] = argv
        cmd['argc'] = len(argv)
        cmd['args'] = ' '.join(argv[1:])
        cmd['help'] = plugins.get(argv[0], 'help')
        cmd['path'] = plugins.get(argv[0], 'path')
        _self.cmd = cmd

        exec(_self.lib_loader())
        exec(_self.load_self_lib())

        try:
            exec( plugins.get(argv[0], 'script') )
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            etype = str(sys.exc_info()[0])
            etype = etype[etype.find('.')+1:-2]
            evalue = str(sys.exc_info()[1])
            if etype == 'SystemExit':
                if evalue:
                    print(evalue)
            else:
                print( P_err+'An error has occured launching the plugin' )
                print( P_err+etype+' : '+evalue )

        _self.env = dict([(x.upper(),y) for x,y in api.env.items()])


    def lib_loader(_self):
        loader = str()
        tpl = ('import pspapi.*\n'
               '* = pspapi.*.*(core, cmd)\n')
        for lib in os.listdir(_self.libs_path):
            if lib.endswith('.py') and lib not in ['__init__.py','self.py']:
                lib = os.path.splitext(lib)[0]
                loader += tpl.replace('*', lib)
        return(loader)


    def load_self_lib(_self):
        loader = 'import pspapi.self as self\n'
        tpl = "self.* = cmd['*']\n"
        for var in _self.cmd:
            loader += tpl.replace('*', var)
        return(loader)
