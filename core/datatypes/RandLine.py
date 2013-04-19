from random import choice as random
from output import colorize
import os.path as path

class RandLine(list):
    """Random line from dynamic buffer. (extends list)

    The random line dynamic buffer (RandLine datatype) handles multiple
    choices from a dynamically managed multiline string buffer.

    It extends the list() mutable built-in python datatype, and its
    raw value is a double elements list. The first one contains the
    parent file (optionnal), while the second element is the current
    string buffer.

    Declaration:
      * A RandLine buffer can be initialized by giving a common string
        as argument, in which case the buffer uses it as value, while
        the parent slot (RandLine()[0]) is set to None, meaning that
        the buffer is static, an not hard disk file based.
      * If the given string starts with the magic prefix "file://",
        then it is assumed the object is file based, it then takes
        the absolute file path as parent (slot 0), and then tries to
        load the file's contents as buffer string, raising an error
        if it fails.
      * Also, for better compatibility with the PhpSploit framework,
        a list instance in the RandLine's standard format (aka
        [<PARENT>, <BUFFER>] is also accepted, and in this case the
        object is simply created, with the given list.

    Dynamic behavior:
      * If the object is file based, the parent will then be checked
        before each __call__() or choices() call, and the buffer
        upgraded if the file is readable AND its content contains at
        least one usable line. Otherwise, the old buffer is silently
        kept.
      * Orphan (with no parent file, aka slot 0 == None) instances
        are static, meaning that the buffer (splot 1) wille never
        change by itself.

    Examples:
    >>> standard = RandLine('file:///etc/passwd')
    >>> standard() # get a random line from current buffer
    "dbus:x:81:81:dbus:/:/sbin/nologin"
    >>> print(standard) # get a nice __str__ representation
    <RandLine@/etc/passwd (24 choices)>
    >>>
    >>> orphan = RandLine('line1\nline2\nline3\n#commented out')
    >>> orphan() # commented line will never be picked
    choice3
    >>> print(orphan) # only valid line choices are considered
    <RandLine (3 choices)>
    >>> print(repr(orphan)) # slot0 None = no parentn slot1 = buffer string
    [None, 'line1\nline2\nline3\n#commented out']

    """

    def __init__(self, value):

        # accept preformated randline raw value (list([parent, buffer]))
        if isinstance(value, list) and len(value) == 2:
            parent, buffer = value
        # otherwise, only string are accepted.
        elif type(value) is not str:
            raise ValueError('must be a string buffer')
        # handle file based buffers
        elif value.lower().startswith('file://'):
            parent = path.expandvars( value[7:] )
            parent = path.realpath( path.expanduser(parent) )
            try:
                buffer = open(parent, 'r').read()
            except:
                raise ValueError('not a readable file: «%s»' %parent)
        # if no source file, set parent=None (orphan RandLine buffer)
        else:
            parent = None
            buffer = value

        # set self value = [parent, buffer] (lists are mutable types)
        self.extend( [parent, buffer] )

        # at least one line on buffer must be usable:
        if not self.choices():
            raise ValueError("couldn't find valid lines from buffer")


    def __call__(self):
        """pick a random line from the valid ones"""
        return random( self.choices() )


    def __str__(self):
        """Get a nice string representation (with terminal colors)
        of the current RandLine object.

        """
        parent = self[0]

        string = colorize("%BoldBlack", "<", "%BoldBlue",
                          "RandLine", "%BasicCyan")

        if parent is not None:
            string += colorize("@", "%Bold", parent)

        string += colorize("%BasicBlue")

        choices = len(self.choices())
        string += " (%s choice%s)" %(choices, ('','s')[choices>1])

        string += colorize("%BoldBlack", ">")

        return string


    def choices(self, target=None):
        """Takes a string as 'target' and return a list of lines from it
        that are not empty or commented (start with #).
        If 'target' is None (which is its default value), then the self
        buffer i used, before trying to get parent file's current value,
        if not orphan, and the file is currently available.

        """
        # if no target string defined, use self buffer, and before
        # try to update the object's parent file (if any)
        if target is None:
            parent = self[0]
            if parent is not None:
                try:
                    newBuffer = open(parent, 'r').read()
                    assert self.choices(newBuffer)
                    self[1] = newBuffer
                except (OSError, AssertionError):
                    pass
            target = self[1]

        # if not none, target MUST be a string
        elif not isinstance(target, str):
            raise ValueError("RandLine.choices(x): must be string or None")

        # treat string an return a list of valid lines
        result = []
        for line in target.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                result.append( line )

        return result
