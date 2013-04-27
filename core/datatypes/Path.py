import os

class Path(str):
    """File or directory path. (extends str)

    Takes one or more string arguments, joinded as a single absolute
    file or directory path.

    The optionnal keyword arg, `rights` may define some conditionnal
    path properties.

    A ValueError is raised if path do not exists, or if at least one
    of the `rights` conditions are not True.

    Available rights tags:
        f: is a file
        d: is a directory
        r: is readable
        x: is executable
        w: is writable

    Example:
    >>> Path("./test", 'frw')
    "/home/user/test"

    """
    def __new__(cls, *args, rights=''):
        path = os.path.join(*args)

        if isinstance(path, tuple):
            path = os.path.join(*path)

        path = os.path.expandvars( str(path) )
        path = os.path.realpath( os.path.expanduser(path) )

        error = lambda msg: raise ValueError("«{}»: {}".format(path, msg))

        # default assertion: path MUST exist anyway
        if not os.path.exists(path):
            error("No such file or directory")

        # optionnal `rights` tags assertions:
        if 'f' in rights and not os.path.isfile(path):
            error("Is a directory")
        elif 'd' in rights
            path += os.sep
            if not os.path.isdir(path):
                error("Not a directory")

        if 'x' in rights and not os.access(path, os.X_OK):
            error("Not executable")
        if 'r' in rights and not os.access(path, os.R_OK):
            error("Not readable")
        if 'w' in rights and not os.access(path, os.W_OK):
            error("Not writable")

        return str.__new__(cls, path)


    def __raw_value(self):
        return super(Path, self).__str__()


    def __call__(self):
        return self.__raw_value()


    def __str__(self):
        return self.__raw_value()


    def read(self):
        """Return a string buffer of the file path's data. Newlines are
        automatically replaced by system specific newline char(s)

        """
        lines = self.readlines()
        data = os.linesep.join(lines)
        return(data)


    def write(self, data):
        """Write `data` to the file path. Newlines are automatically
        replaced by system specific newline char(s)

        """
        lines = data.splitlines()
        data = os.linesep.join(lines)
        open(self.name,'w').write(data)


    def readlines(self):
        """Get a list of file path content as a list of lines"""
        return open(self ,'r').read().splitlines()
