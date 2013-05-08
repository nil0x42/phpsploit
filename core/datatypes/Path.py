import os

class Path(str):
    """File or directory path. (extends str)

    Takes one or more string arguments, joinded as a single absolute
    file or directory path.

    The optionnal keyword arg, `mode` may define some conditionnal
    path properties.

    A ValueError is raised if path do not exists, or if at least one
    of the `mode` conditions are not True.

    Available mode tags:
        e: path exists (default value)
        f: is a file
        d: is a directory
        r: is readable
        x: is executable
        w: is writable

    Example:
    >>> Path("./test", mode='efrw')
    '/home/user/test'
    >>> Path("/home", "user", ".bashrc", mode="fr")
    '/home/user/.bashrc'

    """
    def __new__(cls, *args, mode='e'):
        cls.tmpfile = False

        # if not args, default to random tmp file path:
        if not args:
            try: import session, string, random
            except: raise TypeError("Required 'path' argument(s) not found")
            # get random tmp file path
            randStrChars = string.ascii_lowercase + string.digits
            randStr = "".join( random.choice(randStrChars) for x in range(8) )
            args = (session.Conf.TMPPATH(), "phpsploit-%s.txt" %randStr)
            # create the file with empty content
            open(os.path.truepath(*args), "w").close()
            cls.tmpfile = True # set obj type = tmpfile

        path = os.path.truepath(*args)

        if mode:
            mode += 'e'

        def error(msg):
            raise ValueError("«{}»: {}".format(path, msg))

        # exists
        if 'e' in mode and not os.path.exists(path):
            error("No such file or directory")
        # is file
        if 'f' in mode and not os.path.isfile(path):
            error("Is a directory")
        # is directory
        if os.path.isdir(path):
            path += os.sep
        elif 'd' in mode:
            error("Not a directory")
        # is executable
        if 'x' in mode and not os.access(path, os.X_OK):
            error("Not executable")
        # is readable
        if 'r' in mode and not os.access(path, os.R_OK):
            error("Not readable")
        # is writable
        if 'w' in mode and not os.access(path, os.W_OK):
            error("Not writable")

        return str.__new__(cls, path)


    def _raw_value(self):
        return os.path.realpath( str(self) )


    def __call__(self):
        return os.path.realpath( str(self) )


    def __str__(self):
        return super(Path, self).__str__()


    def __del__(self):
        # remove tmp file
        if self.tmpfile:
            os.unlink(self)

    def edit(self):
        """Try to open file with system's text editor. Return False if the
        edit() method is not available or the file has not changed, and
        return True if the data had been edited.

        """
        try: import session, subprocess
        except: return False

        old = self.read()
        subprocess.call([session.Conf.TEXTEDITOR(), self])
        if self.read() != old:
            return True
        return False


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
        open(self ,'w').write(data)


    def readlines(self):
        """Get a list of file path content as a list of lines"""
        return open(self ,'r').read().splitlines()


class WritableDir(Path):
    def __new__(cls, *args, mode='e'):
        super(WritableDir, cls).__new__(cls, *args, mode='drw')
