import os
import random
import hashlib

from . import MultiLineBuffer
from ui.color import colorize
import utils.path


class RandLineBuffer(MultiLineBuffer):
    """The RandLineBuffer() class provides advanced session Dict item setter.

    It provides multilines buffers, that picks a random choice, and
    dynamic binding from external file paths.

    If a tuple() of list() is given as argument, it's first item will be
    used as object `file` (aka originating file path), and the second
    item will be used as a possibly multiline string representation of
    possible lines.
    EX: RandLineBuffer( ('/tmp/filepath.txt', 'line1\\nline2\\n') )

    If argument is a string whose name starts with "file://", it
    will be assumed a file path was given, putting `file` to this path,
    and `buffer` to the file's content.

    If any other datatype is provided, its string representation will
    be used as possible lines list paragygm.

    Optionnally, the `setfunc` argument (pointer to function) can be
    used in order to ensure that each `buffer` line is syntaxically
    acceptable.

    __str__() provides a nice colored string representation of the
        variable's object.

    __call__() picks a random choice (if multiple), and returns the
        object itself, or it's call if callable.

    __iadd__() adds an awesome behavior: using var+="string" acts adding
        "string" into the var's buffer, considering it as a new possible
        choice.

    __getitem__() allows RandLineBuffer objects being converted to list
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

        # if single choice, make sure choice is valid, trying to pass
        # choice to _getobj, which may return an exception if it fails
        if len(self.buffer.splitlines()) == 1:
            self._getobj(self.buffer.splitlines()[0])

        # if multi choice, at least one line must be usable
        elif not self.choices():
            raise ValueError("couldn't find valid lines from buffer")

    def __call__(self, call=True):
        """Return a random object picked from choices.
        If callable, `obj()` is returned instead of `obj`, only
        if `call` argument is set to True.

        """
        obj = random.choice(self.choices())
        if call and callable(obj):
            return obj()
        return obj

    def __str__(self):
        """Return a color string representation of the setting var object.
        If the buffer has no multiple lines, single choice's string
        representation is returned. Otherwise, the multi line choices
        buffer is represented.

        >>> str( RandLineBuffer("singleChoice") )
        'singleChoice'
        >>> str( RandLineBuffer("file:///etc/passwd") )
        '<RandLine@/etc/passwd (24 choices)>'
        >>> str( RandLineBuffer("choice1\\nchoice2") )
        '<RandLine (2 choices)>'

        """
        # if buffer have one line only, return line string's obj repr
        if not self.file and len(self.buffer.splitlines()) == 1:
            return str(self._getobj(self.buffer.strip()))

        # objID is file path OR buffer's md5sum
        if self.file:
            objID = self.file
        else:
            objID = hashlib.md5(self.buffer.encode('utf-8')).hexdigest()

        # choices is the string that show available choices
        num = len(self.choices())
        choices = " (%s choice%s)" % (num, ('', 's')[num > 1])

        return colorize("%BoldBlack", "<", "%BoldBlue", "RandLine",
                        "%BasicCyan", "@", "%Bold", objID, "%BasicBlue",
                        choices, "%BoldBlack", ">")

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
                try:
                    result.append(self._getobj(line))
                except:
                    continue
        return result
