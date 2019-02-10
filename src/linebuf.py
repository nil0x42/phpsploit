"""Provide advanced line-buffers for phpsploit session settings"""

import os
import hashlib
import random
from abc import ABC, abstractmethod

import utils.path
from ui.color import colorize


class AbstractLineBuffer(ABC):
    r"""Abstract base-class to implement LineBuffer classes

    value (mandatory argument):
    ---------------------------
    If `value` is a tuple() or list():
      - object's 1st item is used as *parent-filepath.
      - object's 2nd item is used as *buffer-data.
        >>> AbstractLineBuffer( ['/tmp/data.txt', 'multi\nline\ncontent'] )

    If `value` is a str() and starts with 'file://':
      - the string after 'file://' is used as *parent-filepath.
      - file's content is used as *buffer-data.
        >>> AbstractLineBuffer("file:///tmp/data.txt")

    Otherwise:
        `str(value)` is used as *buffer-data.
        object is an *orphan-buffer.
        >>> AbstractLineBuffer("nulti\nline\ncontent")


    validator (optional argument):
    ------------------------------
    A `validator` callable (function) can optionally be provided to check
    the validity of buffer's *usable-value.
    It should raise a ValueError() if passed value is invalid.


    Methods:
    --------
    __str__() get a colored string representation of the object.

    __call__() get the *usable-value of the buffer.

    __iadd__() allow strings being concatenated to the end of buffer.
        If string starts with 'file://', object is bound to corresponding
        file path (*file-bound-buffer).

    __getitem__() get elements of object in the form [filepath, buffer].

    _raw_value() get a simple representation of the object, based on python
        built-ins, suitable to be dumped with pickle for later restauration.

    update() try to replace buffer with *parent-filepath's content


    Lexic:
    ------
    *parent-filepath:
        `self.file`
        Filesystem file path string, whose content is used by
        current object to feed *buffer-data.

    *buffer-data:
        `self.buffer`
        A string representing current object's internal data buffer.

    *file-bound-buffer:
        A buffer whose value is taken from a file path (*parent-filepath).
        If file is readable, buffer is upgraded with file content.
        If not readable, current buffer is kept until the file becomes
        accessible again.

    *orphan-buffer:
        A buffer that is not a *file-bound-buffer, i.e. no *parent-filepath
        is defined.

    *usable-value:
        The final value used by phpsploit. It depends on child classes.
        MultilineBuffer() uses the whole buffer as usable value.
        RandLineBuffer() uses a random line from buffer as usable value.
    """

    def __init__(self, value, validator=None):
        if not hasattr(self, "desc"):
            raise NotImplementedError("`desc` (description) attribute"
                                      "is not defined")
        if validator is None:
            validator = (lambda x: x)
        if not callable(validator):
            raise TypeError("`validator` is not callable()")
        self._validator = validator

        if not isinstance(value, (list, tuple)):
            value = str(value)

        # if value is list/tuple:
        if type(value) is not str: # pylint: disable=unidiomatic-typecheck
            self.file = value[0]
            self.buffer = value[1]
        # if value is a 'file://' string
        elif value[7:] and value[:7].lower() == "file://":
            self.file = utils.path.truepath(value[7:])
            try:
                with open(self.file, 'r') as file:
                    self.buffer = file.read()
            except OSError:
                raise ValueError("not a readable file: «%s»" % self.file)
        # if value is just a string
        else:
            self.file = None
            self.buffer = value

    def __call__(self, call=True):
        """Get current buffer's *usable-value

        `call` (bool): If True, and *usable-value is callable,
        return called *usable-value
        """
        usable_value = self._validator(self.buffer)
        if call and callable(usable_value):
            return usable_value()
        return usable_value

    @abstractmethod
    def __str__(self):
        """Get a colored string representation of current object

        >>> MultiLineBuffer("monoline")
        monoline
        >>> MultiLineBuffer("file:///etc/passwd")
        <MultiLine@/etc/passwd (24 lines)>
        >>> MultiLineBuffer("line1\\nline2")
        <MultiLine (2 lines)>
        """

    def __iadd__(self, new):
        """allow strings being concatenated to the end of buffer.
        If string starts with 'file://', suffix is used as new
        *parent-filepath

        >>> x = MultiLineBuffer("choice1")
        >>> x
        choice1
        >>> x += "choice2"
        >>> x += "file:///tmp/foo"
        >>> x
        <MultiLine@/tmp/foo (2 choices)>
        """
        if not isinstance(new, str):
            msg = "Can't convert '{}' object to str implicitly"
            raise TypeError(msg.format(type(new).__name__))

        new += os.linesep
        # if string starts with 'file://', use it as *parent-filepath
        lines = len(new.splitlines())
        if lines == 1 and new[7:] and new[:7] == "file://":
            result = self.__class__(self.buffer, self._validator)
            result.file = new[7:].strip()
            return result
        # otherwise, concatenate normal string to buffer
        buffer = self.buffer
        if buffer[-1] not in "\r\n":
            buffer += os.linesep
        buffer += new
        return self.__class__(buffer, self._validator)

    def __getitem__(self, item):
        """dump object as an iterable of the form:
        [*parent-filepath, *buffer-data]

        >>> tuple(MultiLineBuffer(["/file/path", "buffer"])
        ("/file/path", "buffer")
        """
        if item in [0, "file"]:
            return self.file
        if item in [1, "buffer"]:
            return self.buffer
        raise IndexError(self.__class__.__name__+" index out of range")

    def __getattribute__(self, name):
        """automatically update self.buffer from self.file
        whenever it is possible
        """
        if name == "buffer" and self.file:
            try:
                with open(self.file, 'r') as file:
                    buffer = file.read()
                if self._buffer_is_valid(buffer):
                    self.buffer = buffer
            except OSError:
                pass
        return super().__getattribute__(name)

    def _raw_value(self):
        """convert object into a built-in data type (tuple).
        Format:
        (*parent-filepath, *buffer-data)

        >>> x = MultiLineBuffer("data")
        >>> x._raw_value()
        (None, "data")
        """
        return tuple(self)

    @abstractmethod
    def _buffer_is_valid(self, buffer):
        """check if `buffer` string is valid for current class
        """


# pylint: disable=too-few-public-methods
class MultiLineBuffer(AbstractLineBuffer):
    r"""A LineBuffer supporting multi-line buffers.

    Buffer's *usable-value is set to the whole buffer's content,
    even if it's multi-line.
    """
    desc = r"""
    {var} is a MultiLineBuffer. It supports multi-line buffers.

    * To edit/show buffer with text editor, run this command:
    > set {var} +
    """

    def __init__(self, value, validator=None):
        super().__init__(value, validator)
        self._validator(self.buffer)

    def __str__(self):
        """Get a colored string representation of current object

        >>> MultiLineBuffer("monoline")
        monoline
        >>> MultiLineBuffer("file:///etc/passwd")
        <MultiLine@/etc/passwd (24 lines)>
        >>> MultiLineBuffer("line1\\nline2")
        <MultiLine (2 lines)>
        """
        # if buffer has a single line, use it as representation:
        if not self.file and len(self.buffer.splitlines()) == 1:
            return str(self._validator(self.buffer.strip()))
        # otherwise, use complex representation:
        obj_id = self.file
        if not obj_id:
            obj_id = hashlib.md5(self.buffer.encode('utf-8')).hexdigest()
        lines_str = " (%s lines)" % len(self.buffer.splitlines())
        return colorize("%BoldBlack", "<", "%BoldBlue", "MultiLine",
                        "%BasicCyan", "@", "%Bold", obj_id, "%BasicBlue",
                        lines_str, "%BoldBlack", ">")

    def _buffer_is_valid(self, buffer):
        """return True if buffer is not empty"""
        return bool(buffer.strip())


class RandLineBuffer(AbstractLineBuffer):
    r"""A LineBuffer supporting random-choice multi-line buffers.

    Buffer's *usable-value is set to a random valid choice between
    lines composing the buffer.
    """
    desc = r"""
    {var} is a RandLineBuffer. It supports multiple values.

    If {var} contains multiple lines (choices), a random
    one is used as value each time the setting is used.

    * EXAMPLE:
    The HTTP_USER_AGENT setting has multiple strings as default value.
    Each time an HTTP request is sent, a random User-Agent is used from
    the list of choices (run `set HTTP_USER_AGENT` to show setting).

    * To edit/show buffer with text editor, run this command:
    > set {var} +
    """

    def __init__(self, value, validator=None):
        super().__init__(value, validator)
        if len(self.buffer.splitlines()) == 1:
            # if single choice, submit it to _validator() to validate it
            # important, so real exception is returned in case of failure
            self._validator(self.buffer.splitlines()[0])
        elif not self.choices():
            # if multi choice, at least one line must be usable
            raise ValueError("couldn't find an *usable-choice"
                             " from buffer lines")

    def __call__(self, call=True):
        """Get a random *usable-value from buffer lines.

        `call` (bool): If True, and *usable-value is callable,
        return called *usable-value
        """
        obj = random.choice(self.choices())
        if call and callable(obj):
            return obj()
        return obj

    def __str__(self):
        """Get a colored string representation of current object

        >>> RandLineBuffer("singleChoice")
        singleChoice
        >>> RandLineBuffer("file:///etc/passwd")
        <RandLine@/etc/passwd (24 choices)>
        >>> RandLineBuffer("choice1\\nchoice2")
        <RandLine (2 choices)>
        """
        # if buffer has a single line, use it as representation:
        if not self.file and len(self.buffer.splitlines()) == 1:
            return str(self._validator(self.buffer.strip()))
        # otherwise, use complex representation:
        obj_id = self.file
        if not obj_id:
            obj_id = hashlib.md5(self.buffer.encode('utf-8')).hexdigest()
        num = len(self.choices())
        choices = " (%s choice%s)" % (num, ('', 's')[num > 1])
        return colorize("%BoldBlack", "<", "%BoldBlue", "RandLine",
                        "%BasicCyan", "@", "%Bold", obj_id, "%BasicBlue",
                        choices, "%BoldBlack", ">")

    def _buffer_is_valid(self, buffer):
        """return True if at least one line is a valid
        *usable-choice candidate
        """
        return bool(self.choices(buffer))

    def choices(self, buffer=None):
        """get a list of potential *usable-value lines. I.e. lines
        validated by self._validator().

        Empty lines and comment lines (starting with '#') are ignored.

        If `buffer` argument is None (default), *buffer-data (self.buffer)
        is used.
        """
        if buffer is None:
            buffer = self.buffer
        if not isinstance(buffer, str):
            raise ValueError("`buffer` must be a string")
        # return a list of valid choices only
        result = []
        for line in buffer.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                try:
                    usable_value = self._validator(line)
                except: # pylint: disable=bare-except
                    continue
                result.append(usable_value)
        return result
