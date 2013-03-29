import os
from functions import *

class Load:
    soft_dir = getpath('framework/plugins')

    def __init__(self):
        self.roots = [self.soft_dir]
        self.black_list = list()

        from usr.settings import userDir
        user_dir = getpath(userDir.name, 'plugins')
        try: os.mkdir(user_dir.name)
        except: pass
        if user_dir.isdir():
            self.roots.append(user_dir)


    def update(self):
        """update the plugins list
        """
        categories = self.get_categories()
        self.items = self.get_plugins(categories)


    def blacklist(self, lst):
        """make a name list unusable as plugins
        """
        self.black_list+= lst


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
        """returns the list of plugin names
        owned by the specified category
        """
        items = list()
        for name, item in self.items.items():
            if item['category'] == category:
                items.append(name)
        items.sort
        return items


    def shells(self):
        """get the list of plugins marked as
        usable by the "shell" command
        """
        result = list()
        for name in self.items:
            data = self.items[name]['script']
            if 'api.isshell(' in data:
                result.append(name)
        result.sort()
        return(result)


    def get(self, name, item=None):
        """returns the value of the plugin's item
        """
        if item is None:
            return(self.items[name])

        return(self.items[name][item])



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
                    if  name not in plugins \
                    and name not in self.black_list:
                        elem = self.load_plugin(name, path)
                        if elem:
                            elem['category'] = cat_name
                            elem['path']     = path.name
                            plugins[name] = elem
        return(plugins)


    def load_plugin(self, name, path):
        """load the given plugin "name" at "path".
        The return is False if the given arguments do not match a valid
        PhpSploit plugin. Otherwise, a dictionnary containg the "help"
        and "script" strings is returned.
        """
        if not path.isdir():
            return(False)

        plugin = dict()
        errTpl = P_err+"Error loading %s plugin: plugin.py file " %name
        # try to get the plugin script
        try:
            plugin['script'] = getpath(path.name, "plugin.py").read().strip()
        except:
            print( errTpl + "not found" )
            return(False)
        # check if the script has some content
        if not plugin['script']:
            print( errTpl + "is empty" )
            return(False)
        # load the plugin script's help (docstring)
        plugin['help'] = ""
        scriptCode = compile(plugin['script'], "", "exec")
        if "__doc__" in scriptCode.co_names:
            plugin['help'] = scriptCode.co_consts[0]

        return(plugin)


    def get_categories(self):
        """get the plugin available categories, browsing the plugins dir"""
        categories = dict()

        paths = list()
        for root in self.roots:
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

    def __init__(_self, cmd, plugins, core):
        """ in this class, we use _self instead of self,
        because self is used for the plugins API

        """
        # we add 'help' into the 'self' api object
        cmd['help'] = plugins.get(cmd['name'], 'help')
        cmd['path'] = plugins.get(cmd['name'], 'path')
        _self.cmd = cmd

        exec(_self.lib_loader())
        exec(_self.load_self_lib())

        plugin = plugins.get(cmd['name'], 'script')
        try:
            exec(plugin)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            etype = str(sys.exc_info()[0])
            etype = etype[etype.find('.')+1:-2]
            evalue = str(sys.exc_info()[1])
            if etype == 'SystemExit':
                if evalue: print evalue
            else:
                print P_err+'An error has occured launching the plugin'
                print P_err+etype+' : '+evalue

        _self.env = dict([(x.upper(),y) for x,y in api.env.items()])


    def lib_loader(_self):
        loader = ''
        tpl = 'import pspapi.*\n'
        tpl+= '* = pspapi.*.*(core, cmd)\n'
        for lib in os.listdir(_self.libs_path):
            if lib.endswith('.py') \
            and lib != '__init__.py' \
            and lib != 'self.py':
                lib = os.path.splitext(lib)[0]
                loader+= tpl.replace('*', lib)
        return(loader)


    def load_self_lib(_self):
        loader = 'import pspapi.self as self\n'
        tpl = "self.* = cmd['*']\n"
        for var in _self.cmd:
            loader+= tpl.replace('*', var)
        return(loader)
