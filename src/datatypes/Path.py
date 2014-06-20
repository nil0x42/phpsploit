import os


class Path(str):
    """File or directory path. (extends str)

    Takes one or more string arguments, joinded as a single absolute
    file or directory path.

    The optionnal keyword arg, `mode` defines some conditionnal
    path properties.

    A ValueError is raised if path do not exists, or if at least one
    of the `mode` conditions is not honored.

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
    def __new__(cls, *args, mode='', ext='txt'):
        """Create a new path object.

        The file/dir path is determined by joining `args` as a single
        absolute path.

        virtual undefined path:
        -----------------------
        If args are not specified, a fresh instance wich binds to a
        temporary file is created. The file is generated with a random
        file name which uses `ext` as file extension.

        """

        # if not args, default to random tmp file path:
        if not args:
            import string
            import random
            try:
                from core import session
            except:
                raise TypeError("Required 'path' argument(s) not found")
            # get random tmp file path
            randStrChars = string.ascii_lowercase + string.digits
            randStr = "".join(random.choice(randStrChars) for x in range(12))
            path = session.Conf.TMPPATH() + randStr + "." + ext
            # create the file with empty content
            open(path, "w").close()
        else:
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

    def __init__(self, *args, mode='', ext='txt'):
        # If the datatype takes no arguments, then it is
        # a tmpfile Path() type.
        # Defining its boolean atribute self.tmpfile allows us to
        # unlink the file on object deletion throught __del__().
        if args:
            self.tmpfile = False
        else:
            self.tmpfile = True

    def _raw_value(self):
        return os.path.realpath(str(self))

    def __call__(self):
        return str(self)

    def __str__(self):
        return super().__str__()

    def __del__(self):
        # remove tmp file (if any)
        if self.tmpfile:
            os.unlink(self)

    def edit(self):
        """Open the file with TEXTEDITOR for edition.

        This boolean method returns True if the file had been
        correctly edited, and its content changed.

        The method also fails if the file cannot be edited.
        It may happen if stdin/stdout are not TTYs.

        """
        try:
            import subprocess
            import ui.output
            import ui.input
            from core import session
            assert ui.isatty()
            old = self.read()
            subprocess.call([session.Conf.EDITOR(), self])
            assert self.read() != old
            return True
        except (ImportError, AssertionError):
            return False

    def read(self):
        """Read path file contents.

        NOTE:
        This method actually returns a string formatted for
        the current platform.
        It means that a file contents which uses '\r\n' line
        separators will be returned with '\n' separators
        instead, if it is opened through a GNU/Linux system.

        """
        lines = self.readlines()
        data = os.linesep.join(lines)
        return data

    def write(self, data):
        """Write `data` to the file path.

        Note that newlines are automatically replaced by system
        specific newline char(s).

        """
        lines = data.splitlines()
        data = os.linesep.join(lines)
        open(self, 'w').write(data)

    def readlines(self):
        """Get the list of file path lines.

        NOTE: The lines are returned without newline char(s).

        """
        return open(self, 'r').read().splitlines()

    def phpcode(self):
        """Get minified php code from file.

        Minification:
        The method removes php tag markers ('<?', '?>'),
        empty lines and useless trailing spaces.

        Format:
        The '\n' separator is used, without caring about platform.

        NOTE:
        Multiline comment style (/* foo\nbar */) is not supported
        by internal php code minifier, and should generally not be
        used inside of the phpsploit framework.

        """
        data = self.read().strip()
        if data.startswith('<?php'):
            data = data[5:]
        elif data.startswith('<?'):
            data = data[2:]
        if data.endswith('?>'):
            data = data[:-2]
        data = data.strip()
        result = list()
        for line in data.splitlines():
            line = line.strip()
            if not line.startswith('//'):
                result.append(line)
        return '\n'.join(result)
