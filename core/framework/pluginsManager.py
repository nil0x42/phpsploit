import string, os
from functions import *

class Start:
    validChars        = string.ascii_letters+string.digits+'_'
    descriptionFile   = 'desc.txt'

    def __init__(self):
        self.rootDir = ''
        self.result = dict()
        self.required_files = list()

        self.triggering_elem = None
        self.triggering_elemname = None
        self.triggering_result = None

    def addFileCondition(self, name):
        self.required_files.append(name)


    def Load(self, path):
        self.rootDir = path
        elements = os.listdir(path)
        for name in elements:
            self.triggering_elemname = name
            self.triggering_element = getpath(path, name).name
            if self.checkCurrentElement():
                self.result[name] = self.triggering_result
        return(self.result)


    def checkCurrentElement(self):
        result = dict()
        path = self.triggering_element
        name = os.path.basename(path)

        if not os.path.isdir(path): return(0)
        if name.startswith('.'): return(0)

        if [x for x in name if x not in self.validChars]:
            return self.error('Bad char found in name')

        try: result['description'] = getpath(path, self.descriptionFile).readlines()[0]
        except: return self.error('No description file '+quot(self.descriptionFile))
        if not result['description']: return self.error('Empty description file '+quot(self.descriptionFile))

        for filepath in self.required_files:
            split = filepath.split('/')
            if '.' in split[-1]:
                split[-1] = '.'.join(split[-1].split('.')[:-1])
            name    = ' '.join(split).capitalize()
            varname = '_'.join(split)

            try:
                content = getpath(path, filepath)
                if filepath.lower().endswith('.php'):
                    result[varname] = content.phpcode()
                else:
                    result[varname] = content.read().strip()
            except:
                return self.error(name+' '+quot(filepath)+' (File not found)')

            if not result[varname]:
                return self.error(name+' '+quot(filepath)+' (Empty file)')

        self.triggering_result = result
        return(result)

    def error(self, msg):
        print P_err+'Error loading plugin '+self.triggering_elemname+': '+msg
        return(0)
