"""Phpsploit standard output wrapper.

Usage:
>>> import stdout, sys
>>> sys.stdout = Stdout(backlog=True)
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
"[-] ", it is automatically colored to bright red.

NOTE: Ansi escape codes (terminal colors) are automatically removed
when writting to the backlog.

"""

import sys, re
from io import StringIO
from os import linesep as os_linesep

import ui.output
from ..color import colorize, decolorize

class Stdout:
    """PhpSploit framework's dedicated standard output wrapper,
    supplying some enhancements, such as pattern coloration and
    back logging.

    The 'backlog' argument is defaultly set to False, it can be
    enabled at initialisation if set to True, or enabled later
    setting the instance's backlog attribute to an empty string.

    NOTE: See module's help for more informations.

    NEW: __init__ now also provides a middle proxy from colorama, that
    provides ansi color conversion from ANSI to win terminal codes.

    """

    def __init__(self, outfile=sys.__stdout__, backlog=False):
        # get original stdout
        self._orig_outfile = outfile

        # use the colorama wrapper (ansi to win auto convert) as outfile
        self.outfile = colorama_wrap(self._orig_outfile)

        # handle back logging
        self._backlog = StringIO()
        if backlog:
            self._has_backlog = True
        else:
            self._has_backlog = False

        # are colors supported ?
        self._has_colors = ui.output.colors()


    def __del__(self):
        """Restore the original sys.stdout on Wrapper deletion"""
        self._backlog.close()
        sys.stdout = self._orig_outfile


    def __getattr__(self, obj):
        """Fallback to original stdout objects for undefined methods"""
        return getattr(self._orig_outfile, obj)


    def _writeLn(self, line):
        """Process individual line morphing, and write it"""
        # Process per platform newline transformation
        if line.endswith('\r\n'):
            line = line[:-2] + os_linesep
        elif line.endswith('\n'):
            line = line[:-1] + os_linesep

        line = process_tags(line) # handle tagged lines coloration

        # Write line to stdout, and it's decolorized version on backlog
        # if standard output is not a tty, decolorize anything.
        if self._has_backlog:
            self._backlog.write( decolorize(line) )
        if not self._has_colors:
            line = decolorize(line)
        self.outfile.write( line )


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
            self._backlog.write( decolorize(value) )

    @backlog.deleter
    def backlog(self):
        """Flush backlog buffer and mark it as disabled on deletion"""
        self._backlog.truncate(0)
        self._backlog.seek(0)
        self._has_backlog = False



def process_tags(line):
    """Process tagged line transformations, such as auto colorization
    and pattern rules.

    >>> process_tags("[*] FOO: «bar»\\n")
    '\\x1b[1m\\x1b[34m[*]\\x1b[0m FOO: \\x1b[37m«bar»\\x1b[0m\\n'
    """
    TAGS = [('%BoldBlue',   '[*] '),  # INFO
            ('%BoldRed',    '[!] '),  # ERROR
            ('%BoldPink',   '[?] '),  # QUESTION
            ('%BoldYellow', '[-] ')]  # WARNING

    # return the line as it is if untagged
    for index, tag in enumerate(TAGS):
        if line.startswith(tag[1]):
            break
        if index+1 == len(TAGS):
            return(line)

    # remove dulpicate tags >>> "[!] [!] Foo" -> "[!] Foo"
    while line[len(tag[1]):][0:len(tag[1])] == tag[1]:
        line = line[len(tag[1]):]

    # format line's tag with requested color style
    line = colorize(*tag) + line[len(tag[1]):]


    # colorize «*» patterns from tagged line:
    dye = lambda obj: colorize('%White', "« " + obj.group(1) + " »")
    line = re.sub('«(.+?)»', dye, line)

    # replace angle quotes by double quotes on windws term
    if sys.platform.startswith('win'):
        line = re.sub('«|»', '"', line)

    return line

def colorama_wrap(outfile=sys.__stdout__):
    """Returns an colorama wrap file that acts as an stdout proxy
    between userspace and given output file

    """
    from colorama.initialise import wrap_stream
    return wrap_stream(outfile, None, None, False, True)
