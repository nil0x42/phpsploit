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
feature. It also provides magic output transformation on information
tags. For example, if a line begins with "[-] ", it is automatically
colored to bright red.

NOTE: Ansi escape codes (terminal colors) are automatically removed
when writting to the backlog.
"""
__all__ = ["Stdout"]

import sys
import os
import re
from io import StringIO

import ui.output
from core import encoding
from ..color import colorize, decolorize


class Stdout:
    """PhpSploit framework's dedicated standard output wrapper,
    supplying some enhancements, such as pattern coloration and
    back logging.

    The 'backlog' argument is defaultly set to False, it can be
    enabled at initialization if set to True, or enabled later
    setting the instance's backlog attribute to an empty string.

    NOTE: See module's help for more informations.
    """

    def __init__(self, outfile=sys.__stdout__, backlog=False):
        # get original stdout
        self._orig_outfile = outfile

        # just in case we wrap at runtime o the future,
        # as we did with `colorama_wrapper` in the past
        self.outfile = self._orig_outfile

        # handle back logging
        self._backlog = StringIO()
        if backlog:
            self._has_backlog = True
        else:
            self._has_backlog = False

        # are colors supported ?
        self._has_colors = ui.output.colors()

        self._write_lock = False

    def __del__(self):
        """Restore the original sys.stdout on Wrapper deletion"""
        self._backlog.close()
        # dirty hack when used before argparse on main file...
        sys.stdout = self._orig_outfile
        # try:
        #     sys.stdout = self._orig_outfile
        # except:
        #     pass

    def __getattr__(self, obj):
        """Fallback to original stdout objects for undefined methods"""
        return getattr(self._orig_outfile, obj)

    def _write_line(self, line):
        """Process individual line morphing, and write it"""
        # Process per platform newline transformation
        if line.endswith('\r\n'):
            line = line[:-2] + os.linesep
        elif line.endswith('\n'):
            line = line[:-1] + os.linesep

        # special case: debug tag is only printed if VERBOSITY is True
        # NOTE: considering that the python print() function does another
        #       write() to add line separator, we need a self._write_lock
        #       canary to block it if the previous message display aborted.
        from core import session
        if line.startswith("[#] ") and not session.Conf.VERBOSITY():
            self._write_lock = True
            return
        if self._write_lock:
            self._write_lock = False
            if line == os.linesep:
                return

        line = self.process_tags(line)  # handle tagged lines coloration

        # Write line to stdout, and it's decolorized version on backlog
        # if standard output is not a tty, decolorize anything.
        if self._has_backlog:
            self._backlog.write(decolorize(line))
        if not self._has_colors:
            line = decolorize(line)
        try:
            self.outfile.write(line)
        except UnicodeEncodeError:
            buf = encoding.encode(line)
            self.outfile.buffer.write(buf)

    def write(self, string):
        """Write the given string to stdout"""
        for line in string.splitlines(1):
            self._write_line(line)

    @property
    def backlog(self):
        """A dedicated stdout back logging buffer"""
        if self._has_backlog:
            self._backlog.seek(0)
            return self._backlog.read()
        raise AttributeError()

    @backlog.setter
    def backlog(self, value):
        """Setting backlog's value to None or False disables it,
        While giving any other value resets the backlog buffer.
        If a non empty string is given, backlog takes it as new value
        """
        del self.backlog
        if value is not False and value is not None:
            self._has_backlog = True
        if value.__class__ == str:
            self._backlog.write(decolorize(value))

    @backlog.deleter
    def backlog(self):
        """Flush backlog buffer and mark it as disabled on deletion"""
        self._backlog.truncate(0)
        self._backlog.seek(0)
        self._has_backlog = False

    @staticmethod
    def process_tags(line):
        """Process tagged line transformations, such as auto colorization
        and pattern rules.

        >>> process_tags("[*] FOO: «bar»\\n")
        '\\x1b[1m\\x1b[34m[*]\\x1b[0m FOO: \\x1b[37m«bar»\\x1b[0m\\n'
        """
        tag_list = [('%BoldBlue', '[*] '),   # INFO
                    ('%BoldRed', '[!] '),    # ERROR
                    ('%BoldPink', '[?] '),   # QUESTION
                    ('%BoldYellow', '[-] '), # WARNING
                    ('%BoldBlack', '[#] ')]  # DEBUG

        # if not tagged, return the line as it is
        tag = None # make pylint happy
        for index, tag in enumerate(tag_list):
            if line.startswith(tag[1]):
                break
            if index == len(tag_list) - 1:
                return line

        # remove dulpicate tags >>> "[!] [!] Foo" -> "[!] Foo"
        while line[len(tag[1]):][0:len(tag[1])] == tag[1]:
            line = line[len(tag[1]):]

        # format line's tag with requested color style
        line = colorize(*tag) + line[len(tag[1]):]

        # colorize «*» patterns from tagged line:
        dye = lambda obj: colorize('%White', repr(obj.group(1)))
        line = re.sub('«(.+?)»', dye, line)
        dye = lambda obj: '`' + colorize('%DimWhiteBold', obj.group(1)) + '`'
        line = re.sub('`(.+?)`', dye, line)

        return line
