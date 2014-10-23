import codecs
import base64

import phpserialize

import core
from core import session
from datatypes import Path
from .exceptions import BuildError


def phpserialize_recursive_dict_to_list(python_var):
    if isinstance(python_var, dict):
        if list(python_var.keys()) == list(range(len(python_var))):
            python_var = [python_var[x] for x in python_var]
    if isinstance(python_var, dict):
        for x in python_var:
            python_var[x] = phpserialize_recursive_dict_to_list(python_var[x])
    if isinstance(python_var, list):
        for x in range(len(python_var)):
            python_var[x] = phpserialize_recursive_dict_to_list(python_var[x])
    return python_var


def py2php(python_var):
    serialized = phpserialize.dumps(python_var).decode()
    encoded = Encode(serialized).phpLoader()
    raw_php_var = 'unserialize(%s)' % encoded
    return raw_php_var


def php2py(raw_php_var, bin_mode=False):
    # if bin_mode, raw_php_varis already bytes()..
    if not bin_mode:
        raw_php_var = raw_php_var.encode()
    python_var = phpserialize.loads(raw_php_var, decode_strings=True)
    python_var = phpserialize_recursive_dict_to_list(python_var)
    return python_var


class Encode:
    # call it with Compress(payload, mode)
    # mode compress: force compression
    # mode auto:     compress only if smallest
    # else:          don't compress
    # NOTE: code is a bytes() object !
    def __init__(self, code, mode=''):
        if isinstance(code, str):
            code = bytes(code, "utf-8")
        self.compressed = False
        self.data = b''
        self.decoder = 'base64_decode("%s")'
        if mode in ['compress', 'auto']:
            gzPayload = codecs.encode(code, "zlib")
            gzPayload = base64.b64encode(gzPayload)
            # gzPayload = codecs.encode(gzPayload, "base64")
            gzDecoder = 'gzuncompress(base64_decode("%s"))'
            if mode == 'compress':
                self.compressed = True
                self.data = gzPayload
                self.decoder = gzDecoder
        if mode != 'compress':
            # self.data = codecs.encode(code, "base64")
            self.data = base64.b64encode(code)
        if mode == 'auto':
            if len(gzPayload) < len(self.data):
                self.data = gzPayload
                self.decoder = gzDecoder
        self.data = self.data.decode()
        self.rawlength = len(self.data)
        # patch to get the real urlencoded length of base64
        self.length = self.rawlength
        self.length += self.data.count('/') * 2
        self.length += self.data.count('+') * 2
        self.length += self.data.count('=') * 2

    def phpLoader(self):
        return self.decoder % self.data


class Build:

    encapsulator = Path(core.basedir, 'data/tunnel/encapsulator.php').phpcode()

    def __init__(self, php_payload, parser):

        self.loaded_phplibs = list()

        php_payload = self.encapsulate(php_payload, parser)
        php_payload = self.loadphplibs(php_payload)
        php_payload = self.shorten(php_payload)

        encoded = Encode(php_payload.encode(), 'noauto')

        self.data = encoded.data
        self.length = encoded.length
        self.decoder = encoded.decoder

    def _get_raw_payload_prefix(self):
        """return $PAYLOAD_PREFIX without php tags, in raw format"""

        tmpfile = Path()
        tmpfile.write(session.Conf.PAYLOAD_PREFIX())
        payload_prefix = tmpfile.phpcode()
        del tmpfile
        return payload_prefix

    def encapsulate(self, payload, parser):
        # template encapsulation
        code = self.encapsulator.replace('%%PAYLOAD%%', payload)
        payload_prefix = self._get_raw_payload_prefix()
        code = code.replace("%%PAYLOAD_PREFIX%%", payload_prefix)
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
                libname = line[(line.find('(') + 1):line.find(')')]
                if line.count('(') != 1 or line.count(')') != 1 or not libname:
                    raise BuildError('Invalid php import: ' + line.strip())
                if libname not in self.loaded_phplibs:
                    try:
                        file_path = 'api/php-functions/%s.php' % libname
                        lib = Path(core.coredir, file_path).phpcode()
                    except ValueError:
                        raise BuildError('Php lib not found: ' + libname)
                    result += self.loadphplibs(lib) + '\n'
                    self.loaded_phplibs.append(libname)
        return result

    def shorten(self, code):
        lines = []
        for line in code.splitlines():
            line = line.strip()
            if line and not line.startswith("//"):
                lines.append(line)
        return '\n'.join(lines)
