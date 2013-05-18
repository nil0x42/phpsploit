"""PhpSploit session base class objects.

"""

import os, re, random, hashlib
from ui.color import colorize


class MetaDict(dict):
    """Instanciate an advanced dict() like datatype, especially
    made in order to extend PhpSploit session management taste.

    It may take a dict based object as argument to bind to it.
    Otherwise, it instanciates itself as an empty dictionnary set.


    Magic item access
    -----------------
    The _isattr() method is used as pattern syntax validator on
    __getattribute__() and __setattr__() methods in order to
    respectively use __getitem__() and __setitem__() magic methods
    instead.
    Defaultly, the _isattr() function returns False anyway. This
    means that this nice feature is disabled until overwritten
    by some child class.

    Example:
    An hypothetical child class may enable the item access feature
    explained above by rewritting the _isattr() method like this:
    >>> def _isattr(self, name):
    ...     return name == name.capitalize()

    This way, any called instance attribute whose name is in
    capitalized format will be automagically linked to the self
    dict's corresponding item name, like in the folowing
    concrete case:
    >>> obj = MetaDict({'Foo':'bar', 'baz':'qux'})
    >>> `obj["Foo"]` == `obj.Foo` # those calls are identical
    >>> `obj["baz"]` != `obj.baz` # "baz" != "baz".capitalize()


    Dynamic block display
    ---------------------
    This base class provides a nice dynamic columnized multiline
    string representation of the self dict items. This behavior
    is managed by the __call__() magic method.
    The optionnal argument `pattern` can be used to limit
    item display to keys whose name starts with it's value.
    When displayed, the output string uses self __doc__'s first
    line as title unless alternative title had been provided as
    __init__() named optionnal argument.

    If the self dict does not contains any item, or the pattern
    filter does not match any item name, a ValueError is raised.

    NOTE: Calling the magic __str__() method returns the __call__()
          string result (without `pattern` argument.

    """
    def __init__(self, value={}, title=None):
        # update self dict with `value`
        self.update(value)

        # get object's title string
        if title is not None:
            self.title = str(title)
        else:
            self.title = self.__doc__.splitlines()[0].strip()


    def __getattribute__(self, name):
        # if _isattr(name), then call self getitem
        if name != "_isattr" and self._isattr(name):
            return self.__getitem__(name)

        # otherwise call parent's getattribute
        return super().__getattribute__(name)


    def __setattr__(self, name, value):
        # if _isattr(name), then call self setitem
        if self._isattr(name):
            return self.__setitem__(name, value)

        # otherwise call parent's setattr
        return super().__setattr__(name, value)


    def __setitem__(self, name, value):
        # delete item if self value is empty or None:
        if isinstance(value, (str, type(None))) \
        and str(value).lower() in ["", "none"]:
            return self.__delitem__(name)

        return super().__setitem__(name, value)


    def __dir__(self):
        # considering the special get/set behavior, the __dir__()
        # method must also return self item whose name complies
        # with the self _isattr() boolean function.
        return super().__dir__() + [i for i in self.keys() if self._isattr(i)]


    def _isattr(self, name):
        """Determine whether a called attribute name may be
        considered as an item call. By default, it returns False
        anyway, disabling that feature.

        """
        return False


    def __str__(self):
        """Return self __call__() method"""
        return self.__call__()


    def __call__(self, pattern=""):
        """Nicely display self dict's items as an formatted
        multiline string array.
        The optionnal argument `pattern` can be used to limit
        item display to keys whose name starts with it's value.

        """
        # get matching vars list
        if not self.keys():
            raise ValueError("No such "+self.title)
        keys = [k for k in self.keys() if k.startswith(pattern)]
        if not keys:
            msg = "No such {} matching «{}»"
            raise ValueError( msg.format(self.title ,pattern) )

        # process formatted string
        tpl = ("    {:%s}  {}\n") %max(8, len(max(keys, key=len)))

        buffer = self.title + "\n" + ("=" * len(self.title)) + "\n\n"

        buffer += tpl.format("Variable", "Value")
        buffer += tpl.format("--------", "-----")

        for id, key in enumerate( sorted(keys) ):
            buffer += colorize( ["%Reset", "%Reset"][id%2], \
                                tpl.format(key, self[key]))

        return "\n" + buffer + colorize("%Reset")



class RandLineBuffer:
    """The RandLineBuffer() class provides advanced session Dict item setter.

    It provides multilines buffers, that picks a random choice, and
    dynamic binding from external file paths.

    It takes one required argument, which is the variable's value.
    Alternatively, is a tuple is provided as value, its first element
    will bind to `file`, while the second binds to `buffer`
    EXAMPLE: RandLineBuffer( ('/tmp/filepath.txt', 'line1\\nline2\\n') )

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

    __getitem__() allows RandLineBuffer objects being converted to list
        or tuples as [file, buffer].

    _raw_value() converts the object into a tuple whose first item is
        self.file, while the second is the buffer.
    """
    def __init__(self, value, setfunc=(lambda x:x)):
        self._getobj = setfunc

        if not isinstance(value, (list, tuple)):
            value = str(value)

        # if value is list/tuple, set `file, buffer = value`
        if type(value) is not str:
            self.file =  value[0]
            self.buffer = value[1]
        # elif value is a file:// string
        elif value[7:] and value[:7].lower() == "file://":
            self.file = os.path.truepath(value[7:])
            try: self.buffer = open(self.file, "r").read()
            except: raise ValueError("not a readable file: «%s»" %self.file)
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

        # objID is file path OR buffer's md5sum
        if self.file: objID = self.file
        else: objID = hashlib.md5( self.buffer.encode('utf-8') ).hexdigest()

        # choices is the string that show available choices
        num = len( self.choices() )
        choices = " (%s choice%s)" %(num, ('','s')[num>1])

        return colorize("%BoldBlack", "<", "%BoldBlue", "RandLine",
                        "%BasicCyan", "@", "%Bold", objID, "%BasicBlue",
                        choices, "%BoldBlack", ">")


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
