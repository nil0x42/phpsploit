import base64
import phpserialize

import core
from datatypes import Path
from tunnel.exceptions import BuildError


def py2php(python_var):
    serialized = phpserialize.dumps(python_var)
    encoded = Encode(serialized).phpLoader()
    raw_php_var = 'unserialize(%s)' % encoded
    return raw_php_var


def php2py(raw_php_var):
    python_var = phpserialize.loads(raw_php_var)
    if type(python_var) is dict:
        # The original python var could be a list instead of dict
        # so, we try to convert it to list if it is possible
        try:
            python_var = phpserialize.dict_to_list(python_var)
        except ValueError:
            pass
    return python_var


class Encode:
    # call it with Compress(payload, mode)
    # mode compress: force compression
    # mode auto:     compress only if smallest
    # else:          don't compress
    def __init__(self, code, mode=''):
        self.compressed = False
        self.data = ''
        self.decoder = 'base64_decode("%s")'
        if mode in ['compress', 'auto']:
            gzPayload = base64.b64encode(code.encode('zlib'))
            gzDecoder = 'gzuncompress(base64_decode("%s"))'
            if mode == 'compress':
                self.compressed = True
                self.data = gzPayload
                self.decoder = gzDecoder
        if mode != 'compress':
            self.data = base64.b64encode(code)
        if mode == 'auto':
            if len(gzPayload) < len(self.data):
                self.data = gzPayload
                self.decoder = gzDecoder
        self.rawlength = len(self.data)
        # patch to get the real urlencoded length of base64
        self.length = self.rawlength
        self.length += self.data.count('/')*2
        self.length += self.data.count('+')*2
        self.length += self.data.count('=')*2

    def phpLoader(self):
        return(self.decoder % self.data)


class Build:

    encapsulator = Path(core.basedir, 'data/tunnel/encapsulator.php').phpcode()

    def __init__(self, payload, parser):

        self.loaded_phplibs = list()

        payload = self.encapsulate(payload, parser)
        payload = self.loadphplibs(payload)
        payload = self.shorten(payload)

        encoded = Encode(payload, 'noauto')

        self.data = encoded.data
        self.length = encoded.length
        self.decoder = encoded.decoder

    def encapsulate(self, code, parser):
        # template encapsulation
        code = self.encapsulator.replace('%%PAYLOAD%%', code)
        code = code.rstrip(';') + ';'
        # parser encapsulation
        if parser:
            initCode, stopCode = ['echo "%s";' % x for x in parser.split('%s')]
            code = initCode+code+stopCode
        return code

    def loadphplibs(self, code):
        result = ''
        for line in code.splitlines():
            compLine = line.replace(' ', '')
            if not compLine.startswith('!import('):
                result += line + '\n'
            else:
                libname = line[line.find('(')+1:line.find(')')]
                if line.count('(') != 1 or line.count(')') != 1 or not libname:
                    raise BuildError('Invalid php import: %s' + line.strip())
                if libname not in self.loaded_phplibs:
                    try:
                        file_path = 'api/php/%s.php' % libname
                        lib = Path(core.coredir, file_path).phpcode()
                    except ValueError:
                        raise BuildError('Php lib not found: ' + libname)
                    result += self.loadphplibs(lib)+'\n'
                    self.loaded_phplibs.append(libname)
        return result

    def shorten(self, code):
        lines = []
        for line in code.splitlines():
            line = line.strip()
            if line and not line.startswith("//"):
                lines.append(line)
        result = '\n'.join(lines)
        return result
