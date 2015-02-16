import os
import hashlib

from ui.color import colorize
import utils.path


class MultiLineBuffer:
    """The MultilineLineBuffer() class provides advanced
    session Dict item setter.

    It provides multines buffers, which can be dynamically binded to
    external file paths.

    If a tuple() of list() is given as argument, it's first item will be
    used as object `file` (aka originating file path), and the second
    item as the buffer (which can be multiline).
    EX: MultiLineBuffer( ('/tmp/filepath.txt', 'line1\\nline2\\n') )

    If argument is a string whose name starts with "file://", it
    will be assumed a file path was given, putting `file` to this path,
    and `buffer` to the file's content.

    If any other datatype is provided, its string representation will
    be used as buffer.

    Optionnally, the `setfunc` argument (pointer to function) can be
    used in order to ensure that the buffer syntaxe is acceptable.

    __str__() provides a nice colored string representation of the
        variable's object.

    __call__() This is the proper way to aceed to buffer's contents
        (type string).

    __iadd__() Allows concatenation of the buffer. It means that adding
    the "bar" string to a buffer whose value is "foo" will remain into
    "foo\nbar" (automated newline separation).

    __getitem__() allows MultiLineBuffer objects being converted to list
        or tuples as [file, buffer].

    _raw_value() converts the object into a tuple whose first item is
        self.file, while the second is the buffer.

    """

    def __init__(self, value, setfunc=(lambda x: x)):
        self._getobj = setfunc

        if not isinstance(value, (list, tuple)):
            value = str(value)

        # if value is list/tuple, set `file, buffer = value`
        if type(value) is not str:
            self.file = value[0]
            self.buffer = value[1]
        # elif value is a file:// string
        elif value[7:] and value[:7].lower() == "file://":
            self.file = utils.path.truepath(value[7:])
            try:
                self.buffer = open(self.file, "r").read()
            except:
                raise ValueError("not a readable file: «%s»" % self.file)
        # elif value is just a string
        else:
            self.file = None
            self.buffer = value

        # assert that buffer can be passed to self._getobj (setfunc)
        self._getobj(self.buffer)

    def __call__(self, call=True):
        """Returns the buffer itself (passed to self._getobj())

        If `call` is True and buffer is callable, buffer's call
        is returned instead of the buffer.

        """
        obj = self._getobj(self.buffer)

        if call and callable(obj):
            return obj()
        return obj

    def __str__(self):
        """Return a color string representation of the setting var object.
        If the buffer has no multiple lines, the buffer is just
        represented as a string. Otherwise, multiplie buffer is represented.

        >>> str( MultiLineBuffer("monoline") )
        'monoline'
        >>> str( MultiLineBuffer("file:///etc/passwd") )
        '<MultiLine@/etc/passwd (24 lines)>'
        >>> str( MultiLineBuffer("line1\\nline2") )
        '<MultiLine (2 lines)>'

        """
        # if buffer have one line only, return line string's obj repr
        if not self.file and len(self.buffer.splitlines()) == 1:
            return str(self._getobj(self.buffer.strip()))

        # objID is file path OR buffer's md5sum
        if self.file:
            objID = self.file
        else:
            objID = hashlib.md5(self.buffer.encode('utf-8')).hexdigest()

        lines_str = " (%s lines)" % len(self.buffer.splitlines())
        return colorize("%BoldBlack", "<", "%BoldBlue", "MultiLine",
                        "%BasicCyan", "@", "%Bold", objID, "%BasicBlue",
                        lines_str, "%BoldBlack", ">")

    def __iadd__(self, new):
        """
        >>> x = MultiLineBuffer("choice1")
        >>> x += "choice2"
        >>> x += "file:///tmp/foo"
        >>> str(x)
        '<MultiLine@/tmp/foo (2 choices)>'

        """
        # only strings must be added
        if not isinstance(new, str):
            msg = "Can't convert '{}' object to str implicitly"
            raise TypeError(msg.format(type(new).__name__))

        new += os.linesep
        lines = len(new.splitlines())

        # adding file:// line changes obj's parent file
        if lines == 1 and new[7:] and new[:7] == "file://":
            result = self.__class__(self.buffer, self._getobj)
            result.file = new[7:].strip()
            return result

        # other strings are added to the buffer, and parent file
        # is set to None (because buffer is no more a copy of a file)
        buffer = self.buffer
        if buffer[-1] not in "\r\n":
            buffer += os.linesep
        buffer += new
        return self.__class__(buffer, self._getobj)

    def __getitem__(self, item):
        """It allows the object being converted to list or tuple,
        returning these two elements: [self.file, self.buffer]
        """
        if item in [0, "file"]:
            return self.file
        elif item in [1, "buffer"]:
            return self.buffer
        raise IndexError(self.__class__.__name__+" index out of range")

    def _raw_value(self):
        """Convert the object into a built-in data type (tuple)."""
        return tuple(self)

    def update(self):
        """Try to replace current buffer from parent file (self.file)
        content. If file path is unavailable or None, or file's content
        is empty, the buffer is not changed.

        """
        try:
            buffer = open(self.file, 'r').read()
            assert buffer.strip() != ""
            self.buffer = buffer
        except:
            pass
