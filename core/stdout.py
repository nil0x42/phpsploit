"""Standard Output Wrapper

This class extends and replace the standard python standard output,
aka sys.stdout, and adds some nice multiplatform relative color
support, intellligent buffer forking, and some features really
interesting for the phpsploit framework.

MEMO FOR BUILD:
>>> sys.stdout.__class__.__mro__
(<class '_io.TextIOWrapper'>, <class '_io._TextIOBase'>, <class '_io._IOBase'>, <class 'object'>)


"""

# HOW CAN I CORRECTLY UNHERIT AND EXTEND THE ORIGINAL STDOUT ???
# i want to unherit any stdout's default methods (including isatty(), etc...)
# and only overwrite the ones i want.
# If possible, it will be more clean than manually be forced to define
# all standard stdout methods.


import sys, os, io
import _io

#class Wrapper(_io.TextIOWrapper):
class Wrapper(sys.__stdout__):
    """An stdout wrapper, which handles advanced output features for
    the PhpSploit framework interface.

    """
    def __new__(cls):
        #return( _io.TextIOWrapper.__new__(cls) )
        return( sys.__stdout__.__new__(cls) )


    def __init__(self):
        pass


    def __writeLn(self, line):
        # Handle custom line tags
        tags = {'[*]' : '\033[34;01m',
                '[-]' : '\033[31;01m'}
        for tag, color in tags.items():
            if line.startswith(tag):
                line = color + tag + '\033[0m' + line[len(tag):]
        # Write the treated line with original stdout
        sys.__stdout__.write(line)


    def flush(self):
        pass


    def write(self, data):
        # Each line is treated individually
        for line in data.splitlines(1):
            self.__writeLn( line )




class fork_stdout(object):
    """this class can replace sys.stdout and writes
    simultaneously to standard output AND specified file.

    usage: fork_stdout(altFile)

    """
    def __init__(self, file):
        self.file = file
        self.stdout = sys.stdout
        sys.stdout = self

    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.stdout.flush()

