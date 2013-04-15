"""A standard output (sys.stdout) wrapper.

The provided Wrapper() object is a common python file object,
designed in order to overwrite and extend the standard output,
aka sys.stdout. It has been designed for the PhpSploit framework.

Usage:
>>> import stdout, sys
>>> sys.stdout = stdout.Wrapper(backlog=True)
>>> print("foo")
foo
>>> print("bar")
bar
>>> log = sys.stdout.backlog       # log is now "foo\\nbar\\n"
>>> sys.stdout.backlog = ""        # empty the stdout backlog
>>> print("wtf")
wtf
>>> log = sys.stdout.backlog       # log is now "wtf\\n"
>>> del sys.stdout.backlog         # disable stdout's backlog
>>> sys.stdout.backlog = ""        # enable stdout's backlog

As shown in the example above, the wrapper provides a nice backlog
feature. Considering it's original design, aka enhancing the output
experience for the PhpSplloit Framework, it also provides dynamic
cross-platform pattern coloration. For example, if a line begins with
"[-] ", it is automatically colored to bright red with the "termcolor"
library.

NOTE: Ansi escape codes (terminal colors) are automatically removed
when writting to the backlog.

"""

import sys, re
from io import StringIO
from os import linesep as os_linesep

import termcolor

__all__ = ["Wrapper"]

class Wrapper:
    """PhpSploit framework's dedicated standard output wrapper,
    supplying some enhancements, such as pattern coloration and
    back logging.

    NOTE: See module's help for more informations.

    """
    __dict__ = sys.__stdout__.__dict__

    def __init__(self, backlog=False):
        """Instance initializer"""
        self._backlog = StringIO()
        if backlog:
            self._has_backlog = True
        else:
            self._has_backlog = False


    def __del__(self):
        """Restore the original sys.stdout on Wrapper deletion"""
        self._backlog.close()
        sys.stdout = sys.__stdout__


    def __getattr__(self, obj):
        """Fallback to original stdout objects for undefined methods"""
        return getattr(sys.__stdout__, obj)


    def _writeLn(self, line):
        """Process individual line morphing, and write it"""
        # Process per platform newline transformation
        if line.endswith('\r\n'):
            line = line[:-2] + os_linesep
        elif line.endswith('\n'):
            line = line[:-1] + os_linesep

        line = process_tags(line) # handle tagged lines coloration

        # Write line to stdout, and it's decolorized version on backlog
        sys.__stdout__.write( line )
        if self._has_backlog:
            self._backlog.write( termcolor.blank(line) )


    def write(self, string):
        """Write the given string to stdout"""
        for line in string.splitlines(1):
            self._writeLn( line )


    @property
    def backlog(self):
        """A dedicated stdout back logging buffer"""
        if self._has_backlog:
            self._backlog.seek(0)
            return self._backlog.read()
        else:
            raise AttributeError()

    @backlog.setter
    def backlog(self, value):
        """Setting backlog's value to None or False disables it,
        While giving any other value resets the backlog buffer.
        If a non empty string is given, backlog takes it as new value
        """
        del self.backlog
        if not (value is False or value is None):
            self._has_backlog = True
        if type(value) == str:
            self._backlog.write( termcolor.blank(value) )

    @backlog.deleter
    def backlog(self):
        """Flush backlog buffer and mark it as disabled on deletion"""
        self._backlog.truncate(0)
        self._backlog.seek(0)
        self._has_backlog = False



def process_tags(line):
    """Process tagged line transformations, such as auto colorization
    and pattern rules.

    TAGS is a termcolor.format() syntax string list, if the given line
    starts with the uncolored version of one of them, then the line
    will be considered (an processed) as tagged.

    >>> process_tags("[*] FOO: «bar»\\n")
    '\\x1b[1m\\x1b[34m[*]\\x1b[0m FOO: \\x1b[37m«bar»\\x1b[0m\\n'
    """
    TAGS = ['~{BRIGHT,blue}[*]~{RESET} ',
            '~{BRIGHT,red}[-]~{RESET} ']

    # format tags list to ansi styled strings
    TAGS = [termcolor.format(t) for t in TAGS]

    # return the line as it is if untagged
    for i, tag in enumerate(TAGS):
        blankTag = termcolor.blank(tag)
        if line.startswith(blankTag):
            break
        if i+1 == len(TAGS):
            return(line)

    # colorize the line's tag string
    line = tag + line[len(blankTag):]

    # colorize «*» patterns from tagged line:
    def anglequot_style(matchObj):
        quote = termcolor.draw('white')
        quote += matchObj.group(1)
        quote += termcolor.draw('RESET')
        return quote
    line = re.sub('(«.+?»)', anglequot_style, line)

    # replace angle quotes by double quotes on windws term
    if sys.platform.startswith('win'):
        line = re.sub('«|»', '"', line)

    return line
