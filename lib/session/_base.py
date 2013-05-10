"""PhpSploit session base class objects.

"""

import os, re, random
from ui.color import colorize


class BaseDict(dict):
    """The BaseDict class provides a dict() like base instance for
    simple PhpSploit session variable dictionnaries. It works
    exactly the same way as standard dict() types. Therefore, it
    overwrites the __str__ method, and provides a __call__ method
    also. Both return a nicely formatted list of self contained items.

    NOTE: It is the base class for PhpSploit's `session.Alias` object.

    """
    def __init__(self):
        pass


    def __setitem__(self, name, value):
        """overwrite dict()'s __setitem__ magic method, by calling
        __delitem__ if item's value is in [None, "", "none"].

        """
        if value is None: value = "None"
        if isinstance(value, str) and str(value).lower() in ["", "none"]:
            return self.__delitem__(self, name)
        super(BaseDict, self).__setitem__(name, value)


    def __str__(self):
        """Display the whole items list.
        >>> obj = BaseDict()
        >>> str(obj) # does the same than:
        >>> obj()

        """
        return self.__call__()


    def __call__(self, pattern=""):
        """Display all self items whose name starts with `pattern`.
        By default, it print the whole list.

        """
        keys = [k for k in self.keys() if k.startswith(pattern)]
        tpl = ("    {:%s}  {}\n") %max(8, len(max(keys, key=len)))

        title = self.__doc__.splitlines()[0].strip()
        buffer = title + "\n" + ("=" * len(title)) + "\n\n"

        buffer += tpl.format("Variable", "Value")
        buffer += tpl.format("--------", "-----")

        for id, key in enumerate( sorted(keys) ):
            buffer += colorize( ["%Reset", "%Reset"][id%2], \
                                tpl.format(key, self[key]))

        return "\n" + buffer + colorize("%Reset")




class MetaDict(BaseDict):
    """The MetaDict class extends BaseDict(), and just provides
    a little more functionnality, by making self items gettable
    and settable through attribute access conventions.
    Example:
    >>> obj = MetaDict()
    >>> obj.VAR_NAME # does the same than:
    >>> obj["VAR_NAME"]
    >>> obj.VAR_NAME = "value" # does the same than:
    >>> obj["VAR_NAME"] = "value"

    In the fact, if the called attribute name complies `item_pattern`
    regular expression, the method loops to __setitem__/__getitem__
    magic methods.

    NOTE: It is the base class for PhpSploit's `session.Conf` and
          `session.Env` objects, making settings and environment
          variables callable with `session.Conf.TEXTEDITOR`.

    """
    _item_pattern = re.compile("^[A-Z][A-Z0-9_]+$")

    def __init__(self):
        pass


    def __getattribute__(self, name):
        """Uppercase syntaxically valid names loop to getitem"""
        if name != "_item_pattern" and re.match(self._item_pattern, name):
            return self.__getitem__(name)
        return super(MetaDict, self).__getattribute__(name)


    def __setattr__(self, name, value):
        """Uppercase syntaxically valid names loop to setitem"""
        if re.match(self._item_pattern, name):
            return self.__setitem__(name, value)
        return super(MetaDict, self).__setattr__(name, value)


    def __dir__(self):
        """Append self dict's keys to standard __dir__ method."""
        return super(MetaDict, self).__dir__() + list(self.keys())




class RandLineBuffer:
    """The RandLineBuffer() class provides advanced session Dict item setter.

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

        >>> str( RandLineBuffer("singleChoice") )
        'singleChoice'
        >>> str( RandLineBuffer("file:///etc/passwd") )
        '<RandLine@/etc/passwd (24 choices)>'
        >>> str( RandLineBuffer("choice1\\nchoice2") )
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

        return string


    def __iadd__(self, new):
        """
        >>> x = RandLineBuffer("choice1")
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
            result = RandLineBuffer(self.buffer, self._getobj)
            result.file = new[7:].strip()
            return result

        # other strings are added to the buffer, and parent file
        # is set to None (because buffer is no more a copy of a file)
        if self.buffer[-1] not in "\r\n":
            self.buffer += os.linesep
        self.buffer += new
        return RandLineBuffer(self.buffer, self._getobj)


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
