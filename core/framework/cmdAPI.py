from functions import *
import os, re, sys, string, traceback
import framework.pluginsManager

class Loader:
    core       = dict()
    path       = getpath('framework/commands').name
    validChars = string.ascii_letters+string.digits+'_-'

    def __init__(self):
        return(None)

    def setCore(self, core):
        self.core = core

    def load(self):
        self.update()

    def cmdpath(self, cmd):
        for category in self.elems:
            for name in self.elems[category]:
                if name == cmd:
                    return(getpath(self.path, category+'/'+name).name)

    def cmddata(self, cmd):
        for category in self.elems:
            for name in self.elems[category]:
                if name == cmd:
                    return(self.elems[category][name])

    def update(self):
        self.loader = framework.pluginsManager.Start()
        self.loader.addFileCondition('script.py')
        self.loader.addFileCondition('help.txt')

        self.elems      = dict()
        self.items      = list()
        self.help       = ''
        self.categories = self.loadCategories()
        self.maxlen     = max(13, len(max(self.core.keys(), key=len)))

        self.shells     = list() # the list of commands considered as interactive shells

        reservedNames = self.core.keys()

        for category in self.categories:
            self.elems[category] = dict()
            categoryPath = getpath(self.path, category).name
            categoryCmds = self.loader.Load(categoryPath)

            for cmdName in categoryCmds:
                if cmdName not in reservedNames:
                    if self.maxlen < len(cmdName): self.maxlen = len(cmdName)
                    self.items.append(cmdName)
                    reservedNames.append(cmdName)
                    self.elems[category][cmdName] = categoryCmds[cmdName]

                    if 'api.isshell(' in categoryCmds[cmdName]['script']:
                        self.shells.append(cmdName)

            if not self.elems[category]:
                del self.elems[category]

        self.help = self.loadHelp()

    def loadCategories(self):
        result = list()
        for name in os.listdir(self.path):
            path = getpath(self.path, name).name
            if os.path.isdir(path):
                if [x for x in name if x not in self.validChars]:
                    print P_err+'Bad char found in command category: %s' % quot(name)
                else:
                    result.append(name)
        return(result)

    def loadHelp(self):
        groups = self.elems
        groups['.'] = dict()
        for coreCmd in self.core:
            groups['.'][coreCmd] = {'description': self.core[coreCmd]}

        help = ''
        keys = groups.keys()
        keys.sort()

        for key in keys:
            if key == '.': title = 'Core Commands'
            else: title = 'Pspapi: %s Commands' % key.replace('_',' ').capitalize()
            help+= '\n\n'+title+'\n'+('='*len(title))+'\n\n'
            help+= '    Command'+(' '*(self.maxlen-7+2))+'Description\n'
            help+= '    -------'+(' '*(self.maxlen-7+2))+'-----------\n'
            cmds = groups[key].keys()
            cmds.sort()
            for cmd in cmds:
                help+= '    '+cmd+(' '*(self.maxlen-len(cmd)+2))+groups[key][cmd]['description']+'\n'

        help = '\n'+help.strip()+'\n'
        help.replace('\n',os.linesep)
        return(help)

def Exec(core, cmd, path, name, line):
    core['cmd'] = dict()
    core['cmd']['cwd']  = path
    core['cmd']['help'] = cmd['help']
    core['cmd']['name'] = name
    core['cmd']['argv'] = loadArgs(name+' '+line)
    core['cmd']['argc'] = len(core['cmd']['argv'])

    libsPath = getpath('core/pspapi').name
    libs = [x.split('.')[0] for x in os.listdir(libsPath) if x.endswith('.py')]
    libs = [x for x in libs if x not in ['__init__', 'self']]
    libLoader = 'import pspapi.*\n'
    libLoader+= '* = pspapi.*.*(core)'
    for lib in libs:
        exec(libLoader.replace('*',lib))

    import pspapi.self as self

    for var in core['cmd']:
        exec("self.%s = core['cmd']['%s']" % (var,var))

    try: exec(cmd['script'])

    except:
        etype = str(sys.exc_info()[0])
        etype = etype[etype.find('.')+1:-2]
        evalue = str(sys.exc_info()[1])
        if etype == 'SystemExit':
            if evalue: print evalue
        else:
            print P_err+'An error has occured launching the plugin'
            print P_err+etype+' : '+evalue

    api.env = dict([(x.upper(),y) for x,y in api.env.items()])
    return(api.env)


def loadArgs(line):
    text = line.strip()
    text = text.replace("\\\\","%%ESC_DASLASH%%")
    text = text.replace("'","%%ESC_QUOTE%%")
    text = text.replace("\\ ","%%ESC_SPACE%%")
    args = [x for x in text.split(' ') if x]
    args = [x.replace("%%ESC_SPACE%%"," ") for x in args]
    args = [x.replace("%%ESC_QUOTE%%","\\'") for x in args]
    args = [x.replace("%%ESC_DASLASH%%","\\") for x in args]
    return(args)
