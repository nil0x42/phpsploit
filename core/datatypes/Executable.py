import os
from shutil import which
from output import colorize


class Executable(str):
    """Executable program or shell command. (extends str)

    Takes an executable absolute path or shell command available from
    unix's $PATH env.

    Example:
    >>> Executable('firefox')
    "/usr/bin/firefox"
    >>> path()
    "/usr/bin/firefox"
    >>> print(path)
    "/usr/bin/firefox"

    """
    def __new__(cls, executable):
        abspath = which( str(executable) )
        if abspath is None:
            raise ValueError("«%s» is not an executable program" %executable)
        return str.__new__(cls, abspath)


    def __call__(self):
        return super(Executable, self).__str__()


    def __str__(self):
        path, name = os.path.split(self)
        path += os.sep
        name, ext = os.path.splitext(name)

        return colorize('%Cyan', path, '%BoldWhite', name, '%BasicCyan')
