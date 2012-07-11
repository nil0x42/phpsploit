import os, re, base64
from functions import *

def py2phpVar(var):
    import phpcode.phpserialize
    serialized = phpcode.phpserialize.dumps(var)
    encoded    = Encode(serialized).phpLoader()
    return('unserialize(%s)' % encoded)


class Encode:
    # call it with Compress(payload, mode)
    # mode compress: force compression
    # mode auto:     compress only if smallest
    # else:          don't compress
    def __init__(self, code, mode=''):
        self.compressed = False
        self.data       = ''
        self.decoder    = 'base64_decode("%s")'
        if mode in ['compress','auto']:
            gzPayload = base64.b64encode(code.encode('zlib'))
            gzDecoder = 'gzuncompress(base64_decode("%s"))'
            if mode == 'compress':
                self.compressed = True
                self.data    = gzPayload
                self.decoder = gzDecoder
        if mode != 'compress':
            self.data = base64.b64encode(code)
        if mode == 'auto':
            if len(gzPayload) < len(self.data):
                self.data    = gzPayload
                self.decoder = gzDecoder
        self.rawlength = len(self.data)
        # patch to get the real urlencoded length of base64
        self.length = self.rawlength
        self.length+= self.data.count('/')*2
        self.length+= self.data.count('+')*2
        self.length+= self.data.count('=')*2
    def phpLoader(self):
        return(self.decoder % self.data)


class Build:

    encapsulator = getpath('framework/phpfiles/encapsulator.php').phpcode()

    def __init__(self, payload, parser):

        self.error = ''
        self.loaded_phplibs = list()

        payload = self.encapsulate(payload, parser)
        payload = self.loadphplibs(payload)
        payload = self.shorten(payload)

        encoded = Encode(payload, 'noauto')

        self.data    = encoded.data
        self.length  = encoded.length
        self.decoder = encoded.decoder
        self.error   = self.error.strip()

    def encapsulate(self, code, parser):
        # template encapsulation
        code = self.encapsulator.replace('%%PAYLOAD%%', code)
        code = code.rstrip(';')+';'
        # parser encapsulation
        if parser:
            initCode, stopCode = ['echo "%s";' % x for x in parser.split('%s')]
            code = initCode+code+stopCode
        return(code)

    def loadphplibs(self, code):
        result = ''
        for line in code.splitlines():
            compLine = line.replace(' ','')
            if not compLine.startswith('!import('):
                result+= line+'\n'
            else:
                libname = line[line.find('(')+1:line.find(')')]
                if line.count('(') != 1 or line.count(')') != 1 or not libname:
                    self.error+= 'Invalid php import: '+line.strip()+P_NL
                    return('')
                if libname not in self.loaded_phplibs:
                    try:
                        lib = getpath('framework/phplibs/%s.php' % libname).phpcode()
                    except:
                        self.error+= 'Php lib not found: '+libname+P_NL
                        return('')
                    result+= self.loadphplibs(lib)+'\n'
                    self.loaded_phplibs.append(libname)
        return(result)

    def shorten(self, code):
        return('\n'.join([x.strip() for x in code.splitlines() if x.strip() and not x.strip().startswith('//')]))
