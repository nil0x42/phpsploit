import os
import sys
import importlib

from datatypes import Path

from .exceptions import InvalidPlugin, UnloadablePlugin


class Plugin:
    """Phpsploit plugin class

    This object instanciates a new plugin object.

    Example:
    >>> plugin = Plugin("./plugins/file_system/ls")
    >>> plugin.name
    'ls'
    >>> plugin.category
    'File system'
    >>> plugin.run(['ls', '-la'])  # run the plugin with args

    """

    def __init__(self, path):
        if path.endswith("/"):
            path = path[:-1]

        # name
        self.name = os.path.basename(path)

        # path
        self.path = path

        try:
            self.path = Path(path, mode='drx')()
        except ValueError as e:
            raise InvalidPlugin(self.name + ": " + e)

        # category
        category = os.path.basename(os.path.dirname(path))
        self.category = category.replace(" ", "_").capitalize()

        # script
        try:
            self.script = Path(path, "plugin.py", mode='fr').read()
        except:
            raise UnloadablePlugin("file not found")
        if not self.script.strip():
            raise UnloadablePlugin("file is empty")

        # help
        self.help = ""
        try:
            code = compile(self.script, "", "exec")
        except SyntaxError as e:
            raise UnloadablePlugin("compilation failed")
        if "__doc__" in code.co_names:
            self.help = code.co_consts[0]

    def run(self, argv):

        try:
            ExecPlugin(self)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except:
            etype = str(sys.exc_info()[0])
            etype = etype[(etype.find('.') + 1):-2]
            evalue = str(sys.exc_info()[1])
            if etype == 'SystemExit':
                if evalue:
                    print(evalue)
            else:
                print('[-] An error has occured launching the plugin')
                print("[-] %s : %s" % (etype, evalue))


class ExecPlugin:

    filename = "plugin"
    _instance_id = 0

    def __init__(self, plugin):
        script_path = os.path.join(plugin.path, self.filename + ".py")
        sys.path.insert(0, plugin.path)
        try:
            self.exec_module(script_path)
        finally:
            sys.path.pop(0)

    @classmethod
    def is_first_instance(cls):
        if cls._instance_id == 0:
            result = True
        else:
            result = False
        cls._instance_id += 1
        return result

    def exec_module(self, path):
        loader = importlib.machinery.SourceFileLoader(self.filename, path)
        module = importlib.import_module(self.filename)

        # If the instance is the first one, it means that
        # the import already executed the plugin.
        if not self.is_first_instance():
            loader.exec_module(module)
