import os

class Path(str):
    """Writable absolute directory path. (extends str)

    Take a file or directory path. It will be automatically converted
    to an absolute path. If a tuple of strings is given, then the
    elements will be joined as a single path string.

    The optionnal `rights` argument may be used to add some path
    attributes conditions.

    A ValueError is raised is path do not exists, or if at least one
    of the `rights` tags are not True.

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
    def __new__(cls, path, rights=''):
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

        return str.__new__(cls, path+os.sep)


    def __raw_value(self):
        return super(Path, self).__str__()


    def __call__(self):
        return self.__raw_value()


    def __str__(self):
        return self.__raw_value()
