"""PhpSploit framework's stdout manager.
"""


import sys, io
import termcolor


class Wrapper:
    """A custom file object designed to wrap the standard sys.stdout
    on the PhpSploit framework environment. Additionally to acts as
    the standard one, it features a backlog (colorless), and dynamic
    cross-platform pattern coloration.

    >>> import sys
    >>> sys.stdout = stdout.Wrapper() # define the new stdout
    >>> print('foo\nbar')             # print something
    foo
    bar
    >>> log = sys.stdout.backlog      # save the back log
    foo
    bar
    >>> del sys.stdout.backlog        # flush the back log
    >>> del sys.stdout                # restore original stdout

    """
    __dict__ = sys.__stdout__.__dict__


    def __init__(self):
        """Initialize self instance and it's dedicated backlog"""
        self._backlog = io.StringIO()


    def __del__(self):
        """Restore the original sys.stdout on Wrapper deletion"""
        self._backlog.close()
        sys.stdout = sys.__stdout__


    def __getattr__(self, obj):
        """Fallback to original stdout objects for undefined methods"""
        return( getattr(sys.__stdout__, obj) )


    def _writeLn(self, line):
        """Process individual line morphing, and write it"""
        # Handle custom line tags
        tags = {'[*]' : '\033[34;01m',
                '[-]' : '\033[31;01m'}
        for tag, color in tags.items():
            if line.startswith(tag+" "):
                line = color + tag + '\033[0m ' + line[len(tag):]

        # Write line to stdout, and it's decolorized version on backlog
        sys.__stdout__.write( line )
        self._backlog.write( termcolor.decolorize(line) )


    def write(self, string):
        """Write the given string to stdout"""
        for line in string.splitlines(1):
            self._writeLn( line )


    @property
    def backlog(self):
        """Hook method called on backlog getting"""
        self._backlog.seek(0)
        return( self._backlog.read() )


    @backlog.deleter
    def backlog(self):
        """Hook method called on backlog deletion"""
        self._backlog.truncate(0)
