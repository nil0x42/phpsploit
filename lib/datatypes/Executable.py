import os
from shutil import which
from ui.color import colorize


class Executable(str):
    """Executable program or shell command. (extends str)

    Takes an executable program path or shell command.

    >>> browser = Executable('firefox')
    >>> browser()
    "/usr/bin/firefox"

    """
    def __new__(cls, executable):
        abspath = which( str(executable) ) # use shutil.which
        if abspath is None:
            raise ValueError("«%s» is not an executable program" %executable)
        return str.__new__(cls, abspath)


    def _raw_value(self):
        return super(Executable, self).__str__()


    def __call__(self):
        return self._raw_value()


    def __str__(self):
        path, name = os.path.split(self)
        path += os.sep
        name, ext = os.path.splitext(name)

        return colorize('%Cyan', path, '%BoldWhite', name, '%BasicCyan')
