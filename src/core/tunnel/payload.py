import codecs
import base64

import phpserialize

import core
from core import session
from core import encoding
from datatypes import Path
from .exceptions import BuildError


def phpserialize_recursive_dict_to_list(python_var):
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
        for x in python_var:
            python_var[x] = phpserialize_recursive_dict_to_list(python_var[x])
    if isinstance(python_var, list):
        for x in range(len(python_var)):
            python_var[x] = phpserialize_recursive_dict_to_list(python_var[x])
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
    python_var = phpserialize_recursive_dict_to_list(python_var)
    return python_var


class Encode:
    """Take a php code string, and convert it into
    an encoded payload, for easily mergind it into
    an existing php payload.
    This class also provides payload size minification
    by using gzip compression.

    USAGE
    =====
    Encodings:
    ----------
    * base64:
        The payload it base64 encoded, an wrapped into
        the php `base64_decode()` function.

    * gzip + base64:
        The payload is compressed with zlib, then the
        compressed payload is base64 encoded.

    Modes:
    ------
    * default:
        base64 encode only;

    * auto:
        base64 encode, and compress with zgip only
        if resulting payload is really smaller than
        without compression.

    * compress:
        base64 encode, and force usage of compression.

    ATTRIBUTES
    ==========
    * decoder (str)
        payload decoder for self.data payload.
        example: 'base64_decode(%s)'

    * data (str):
        encoded payload string, without it's decoder
        it always contains a simple base64 stream.

    * rawlength (int):
        same as `len(data)`.

    * length (int):
        amout of bytes the payload will take when
        copied into an HTTP request.

    * compressed (bool):
        True if encoder has been compressed.

    METHODS
    =======
    * php_loader() (str)
        Returns current payload string, wrapped with decoder.
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
                self.compressed = True
        self.data = self.data.decode()
        self.rawlength = len(self.data)
        self.length = self.get_real_transport_length(self.data)

    def php_loader(self):
        """Returns the php_loader for encoded phpcode string.
        """
        return self.decoder % self.data

    def get_real_transport_length(self, payload):
        """Get real length the given data payload takes
        while transported via HTTP with urlencoding.
        Indeed, base64 payloads contain 3 types of chars which
        are urlencoded, as urlencoding makes the encoded char 3
        times larger, we should add it to length.
        """
        length = len(payload)
        length += payload.count('/') * 2
        length += payload.count('+') * 2
        length += payload.count('=') * 2
        return length


class Build:
    """Generate final payload, as it can be injected into http requests.

    The returned string includes `parser`, the separation tags allowing
    tunnel handler to retrieve output returned from payload after
    remote http request execution.

    The payload is also encapsulated through phpsploit standard
    encapsulator (./data/tunnel/encapsulator.php).
    """
    encapsulator = Path(core.basedir, 'data/tunnel/encapsulator.php').phpcode()

    def __init__(self, php_payload, parser):

        self.loaded_phplibs = list()

        php_payload = self.encapsulate(php_payload, parser)
        php_payload = self.loadphplibs(php_payload)
        php_payload = self.shorten(php_payload)

        encoded_payload = Encode(php_payload.encode(), 'noauto')

        self.data = encoded_payload.data
        self.length = encoded_payload.length
        self.decoder = encoded_payload.decoder

    def _get_raw_payload_prefix(self):
        """return $PAYLOAD_PREFIX without php tags, in raw format
        """
        tmpfile = Path()
        tmpfile.write(session.Conf.PAYLOAD_PREFIX())
        payload_prefix = tmpfile.phpcode()
        del tmpfile
        return payload_prefix

    def encapsulate(self, payload, parser):
        """Wrap the given payload with `parser` tags, so the payloads
        prints those tags into the page at remote php runtime, allowing
        the tunnel handler to grab payload response from returned
        web page.
        """
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
        """Replace `!import(<FOO>)` special syntax with real
        local library files.
        """
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
        """Trivial code minifier for payload size optimization.
        """
        lines = []
        for line in code.splitlines():
            line = line.strip()
            if line and not line.startswith("//"):
                lines.append(line)
        return '\n'.join(lines)
