import os

class WritableDir(str):
    """Writable absolute directory path. (extends str)

    Take a path as argument, it must be a standard directory with
    write privileges, and will be converted into an absolute path.

    Example:
    >>> WriteblaDir("./test")
    "/home/user/test"

    """
    def __new__(cls, path):
        path = os.path.expandvars( str(path) )
        path = os.path.realpath( os.path.expanduser(path) )

        if not os.path.exists(path):
            raise ValueError("«%s» path does not exist" %path)
        if not os.path.isdir(path):
            raise ValueError("«%s» is not a directory" %path)
        if not os.access(path, 2):
            raise ValueError("«%s» is not writable" %path)

        return str.__new__(cls, path+os.sep)


    def __raw_value(self):
        return super(Executable, self).__str__()


    def __call__(self):
        return self.__raw_value()


    def __str__(self):
        return super(WritableDir, self).__str__()
