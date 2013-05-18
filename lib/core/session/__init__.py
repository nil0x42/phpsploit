"""PhpSploit Session Manager

When imorted for the first time, the "session" package initializes it
self as a PhpSploit blank session, with its default values.


Provide the PhpSploit framework's session object from Session() class.
On import, an instance of it is defaultly created as `session`.

A session instance contains the following objects:
    * Conf  -> The configuration settings
    * Env   -> Tunnel related environment variables
    * Alias -> User's command aliases
    * File  -> The default file that binds to session
    * Cache -> Remote server response cache
    * Hist  -> Readline history

"""
import os, re, gzip, pickle

import ui.input, backwards.session
from datatypes import Path
from ui.color import colorize

from . import baseclass
from . import settings
from . import environment

SESSION_FILENAME = "phpsploit.session"

class Session(baseclass.MetaDict):
    """Phpsploit Session

    """
    def __init__(self):
        """Instanciate the phpsploit session, it handles configuration
        settings, environment variables, command aliases, http response
        cache and readline history (if readline is available).

        """
        # process parent class init
        super().__init__()

        # session objects declaration
        self.Conf = settings.Settings()
        self.Env = environment.Environment()
        self.Alias = baseclass.MetaDict(title="Command Aliases")
        self.Cache = baseclass.MetaDict(title="HTTP Response Cache")
        self.File = None


    def _isattr(self, name):
        """Session items are alphabetic and capitalized strings"""
        return re.match("^[A-Z][a-z]+$", name)


    def __getitem__(self, name):
        """Overwrite standard getitem to return self.File
        default dynamic value in the case it is None.
        """
        value = super().__getitem__(name)
        if name == "File" and value is None:
            value = self.Conf.SAVEPATH() + SESSION_FILENAME
        return value


    def __setitem__(self, name, value):
        # use grandparent class (bypass parent's None feature)
        dict.__setitem__(self, name, value)


    def __str__(self):
        """Gives a nice string representation of current session"""
        title = "PhpSploit session dump ({})".format(self.File)
        deco = "\n" + colorize("%Blue", "=" * len(title)) + "\n"
        data = deco + title + deco
        for obj in self.values():
            if isinstance(obj, baseclass.MetaDict):
                try: data += str(obj) + "\n"
                except: pass
        return data


    def __call__(self, file=None):
        """Load and return the session object stored in `file`.
        if `file` is None, current session (self) is returned.

        """
        # A None/empty call returns current session as it is
        if file is None:
            return self

        file = os.path.truepath(file)
        # append default filename is is a directory
        if os.path.isdir(file):
            file = os.path.truepath(file, SESSION_FILENAME)

        # create a new empty session
        session = Session()

        # get unpickled `data` from `file`
        try:
            data = pickle.load( gzip.open(file) )
        except OSError as e:
            if str(e) != "Not a gzipped file":
                raise e
            backwards.session.load(file)
            try:
                data = backwards.session.load(file)
                import pprint
                pprint.pprint(data)
                assert data.keys() == session.keys()
            except:
                raise Warning("not a session file", "«{}»".format(file))

        # fill it with loaded file data
        for key in session.keys():
            if isinstance(key, dict):
                session[key].update( data[key] )
            else:
                session[key] = data[key]
        # bind new session's File to current file
        session.File = file

        return session


    def update(self, obj=None):
        """Update current session with `obj`.
        The given argument can be a dictionnary instance, in which case
        it must be a valid session object to merge in.
        If `obj` is a string, it is then considered as a file path, and
        the self __call__() method is then used in order to retrieve
        corresponding session object.
        Is `obj` is None (default), then "./phpsploit.session" is used.

        """
        if obj is None:
            obj = "./" + SESSION_FILENAME
        # if obj is a string, get path's session from self call
        if isinstance(obj, str):
            obj = self(obj)
        # if obj is not a dict instance, fallback to parent method
        if not isinstance(obj, dict):
            return super().update(obj)

        for key, value in obj.items():
            if isinstance(self[key], dict):
                self[key].update(value)
            else:
                self[key] = value


    def dump(self, file=None):
        """Dump current session to `file`.
        `file` defaults to self.File if unset.
        """
        if file is None:
            file = self.File

        # if file is a filename only, use SAVEPATH as root directory
        if not os.sep in file:
            file = self.Conf.SAVEPATH() + file

        # get file's absolute path
        file = os.path.truepath(file)

        # if it is a directory, append default session file name
        if os.path.isdir(file):
            file = os.path.truepath(file, SESSION_FILENAME)

        # if file exists and differs from session's binded file,
        # then an user overwriting confirmation is required.
        if os.path.exists(file) and file != self.File:
            question = "File «{}» already exists, overwrite it ?"
            if ui.input.Expect(False)( question.format(file) ):
                raise Warning("The session was not saved")

        # get a simplified copy of current session that
        # only contains python built-in objects:
        rawdump = {}
        for object in self.keys():
            rawdump[object] = {}
            rawvar = (tuple if object == "Conf" else str)
            if isinstance(self[object], dict):
                for var, value in self[object].items():
                    rawdump[object][var] = rawvar(value)
            else:
                rawdump[object] = rawvar(self[object])

        # write it to the file
        pickle.dump(rawdump, gzip.open(file, 'wb'))




# instanciate main phpsploit session as core.session
session = Session()
