import os

from core import encoding
import utils.path


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
    def __new__(cls, *args, mode='', filename='file.txt'):
        """Create a new path object.

        The file/dir path is determined by joining `args` as a single
        absolute path.

        virtual undefined path:
        -----------------------
        If no path arguments are specified, a fresh instance which
        binds to a temporary file is created. A random directory
        name is created into TMPPATH, and file name unherits the
        `filename` class argument which defaults to 'file.txt'.
        Example:
            >>> from core import session
            >>> session.Conf.TMPPATH = "/tmp"
            >>> path = Path()
            >>> print(path)
            /tmp/Iej4iephaeci/file.txt
            >>> path = Path(filename="code.php")
            >>> print(path)
            /tmp/baeW7OoChooF/code.php

        """
        # if not args, default to random tmp file path:
        if not args:
            import uuid
            try:
                from core import session
            except:
                raise TypeError("Required 'path' argument(s) not found")
            # get random tmp file path
            rand_dir = str(uuid.uuid4()) + os.sep
            filename = filename.replace(os.sep, "")  # remove '/' from filename
            path = session.Conf.TMPPATH() + rand_dir + filename
            os.makedirs(os.path.dirname(path))
            # create the file with empty content
            open(path, 'w+').close()
        else:
            path = utils.path.truepath(*args)

        if mode:
            mode += 'e'

        def error(msg):
            raise ValueError("%r: %s" % (path, msg))

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

    def __init__(self, *args, mode='', filename='file.txt'):
        """Instanciate a new Path()

        Instance is considered a tmpfile (temporary file) if
        called without arguments.
        It means that the linked file will be automatically
        deleted from filesystem at object deletion (self.__del__()).
        """
        # If the datatype takes no arguments, then it is
        # a tmpfile Path() type.
        # Defining its boolean atribute self.tmpfile allows us to
        # unlink the file on object deletion throught __del__().
        self.tmpfile = not args

    def _raw_value(self):
        return os.path.realpath(str(self))

    def __call__(self):
        return str(self)

    def __del__(self):
        # remove tmp file (if any)
        if self.tmpfile:
            os.unlink(self)
            try:
                os.rmdir(os.path.dirname(self))
            except OSError:
                pass

    def edit(self):
        """Open the file with EDITOR setting for edition.

        This boolean method returns True if the file has been
        correctly edited, and its content changed.
        """
        from core import session
        import subprocess
        import shlex

        # We use shlex not shnake because we need something naive.
        # We don't want to handle redirection and other stuff.
        args = shlex.split(session.Conf.EDITOR())
        args.append(self)

        old = self.read(bin_mode=True)
        try:
            subprocess.call(args)
        except OSError:
            print("[-] Invalid EDITOR (fix with `set EDITOR <value>`)")
            raise
        new = self.read(bin_mode=True)
        return new != old

    def browse(self):
        """Display the file through phpsploit's BROWSER

        NOTE: For the moment, the method always returns True,
              but it may chance in the future.
        """
        from core import session

        return session.Conf.BROWSER(call=False).open(self)

    def read(self, bin_mode=False):
        """Read path file contents.

        This method actually returns a string formatted for
        the current platform.
        It means that a file contents which uses '\r\n' line
        separators will be returned with '\n' separators
        instead, if it is opened through a GNU/Linux system.

        If you want to read data rawly, without newline treatment
        as mentionned above, the bin_mode optionnal argument
        should be set to True, in which case a bytes() buffer
        containing file data is returned instead of str().

        """
        if bin_mode:
            with open(self, 'rb') as file:
                return file.read()
        else:
            try:
                lines = self.readlines()
                return os.linesep.join(lines)
            except UnicodeDecodeError:
                bytestring = self.read(bin_mode=True)
                return encoding.decode(bytestring)

    def write(self, data, bin_mode=False):
        """Write `data` to the file path.

        If bin_mode is True or data is a bytes() object,
        data is rawly written to the file in binary mode.

        Otherwise, data must be of type str(), and a pre treatmen
        is applied to the buffer, replacing line separators with
        system specific newline char(s).

        Note that newlines are automatically replaced by system
        specific newline char(s) is data is a string.
        Otherwise, is data is a bytes() buffer, data is rawly written.

        """
        if isinstance(data, bytes):
            bin_mode = True

        if not bin_mode:
            try:

                lines = data.splitlines()
                data = os.linesep.join(lines)
                with open(self, 'w') as file:
                    file.write(data)
                return
            except UnicodeDecodeError:
                bin_mode = True

        if bin_mode:
            # if bin_mode, convert str() to bytes()
            if isinstance(data, str):
                data = encoding.encode(data)
            # otherwise, try to convert to bytes()
            elif not isinstance(data, bytes):
                data = bytes(data)
            with open(self, 'wb') as file:
                file.write(data)
            return

    def readlines(self):
        """Get the list of file path lines.

        NOTE: The lines are returned without newline char(s).

        """
        with open(self, 'r') as file:
            return file.read().splitlines()

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
