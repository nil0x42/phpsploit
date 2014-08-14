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
import os
import re
import gzip
import copy
import pickle
import difflib

import ui.input
import objects
import backwards.session
from ui.color import colorize, decolorize

from . import settings
from . import environment
from . import history

SESSION_FILENAME = "phpsploit.session"


class Session(objects.MetaDict):
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
        self.Env = {}
        self.Alias = objects.VarContainer(title="Command Aliases")
        self.Cache = objects.VarContainer(title="HTTP Response Cache")
        self.Hist = history.History()
        self.File = None

    def _isattr(self, name):
        """Session items are alphabetic and capitalized strings"""
        return re.match("^[A-Z][a-z]+$", name)

    def _history_update(self, array=[]):
        try:
            import readline
            # add array elements to readline history
            for command in array:
                # print("add: "+repr(command))
                readline.add_history(command)
            # recreate Hist from readline history (UGLY)
            self.Hist.clear()
            for i in range(1, readline.get_current_history_length() + 1):
                # print("current item: "+repr(readline.get_history_item(i)))
                self.Hist.append(readline.get_history_item(i))
        except ImportError:
            pass
        # By default, hist max size is 20% of CACHE_SIZE
        max_size = int(self.Conf["CACHE_SIZE"]() * 0.2)
        # Settle Hist object to its max size
        while self.Hist.size > max_size:
            self.Hist.pop(0)

    def __getitem__(self, name):
        """Overwrite standard getitem to return self.File
        default dynamic value in the case it is None.
        """
        value = super().__getitem__(name)
        if name == "File":
            if value is None:
                value = self.Conf.SAVEPATH() + SESSION_FILENAME
            elif not os.path.isdir(value) and os.sep not in value:
                value = self.Conf.SAVEPATH() + value
        return value

    def __setitem__(self, name, value):
        # use grandparent class (bypass parent's None feature)
        # setting Env item has special wrap
        if name == "Env":
            value = environment.Environment(value)
        dict.__setitem__(self, name, value)

    def __str__(self):
        """Gives a nice string representation of current session"""
        title = "PhpSploit session dump ({})".format(self.File)
        # deco = "\n" + colorize("%Blue", "=" * len(title)) + "\n"
        deco = "\n" + colorize("%Blue", "=" * 68) + "\n"
        data = deco + title + deco
        for obj in self.values():
            if isinstance(obj, objects.MetaDict):
                try:
                    data += str(obj) + "\n"
                except:
                    pass
        return data

    def __call__(self, file=None):
        """Load and return the session object stored in `file`.
        if `file` is None, current session (self) is returned.

        """
        # A None/empty call returns current session as it is
        if file is None:
            return self

        file = os.path.truepath(file)
        # append default filename if is a directory
        if os.path.isdir(file):
            file = os.path.truepath(file, SESSION_FILENAME)

        # create a new empty session
        session = Session()

        # get unpickled `data` from `file`
        try:
            data = pickle.load(gzip.open(file))
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
                session[key].update(data[key])
            elif key != "Hist":
                session[key] = data[key]
        try:
            session._history_update(data["Hist"])
        except:
            pass
        # bind new session's File to current file
        session.File = file

        return session

    def load(self, file=None):
        return (self(file))

    def update(self, obj=None):
        """Update current session with `obj`.
        The given argument can be a dictionnary instance, in which case
        it must be a valid session object to merge in.
        If `obj` is a string, it is then considered as a file path, and
        the self __call__() method is then used in order to retrieve
        corresponding session object.
        Is `obj` is None (default), "${SAVEPATH}./phpsploit.session" is used.

        """
        if isinstance(obj, str):
            obj = self.load(obj)

        elif obj is None:
            obj = self.load(self.File)

        # if obj is not a dict instance, fallback to parent method
        elif not isinstance(obj, dict):
            return super().update(obj)

        for key, value in obj.items():
            if isinstance(self[key], dict):
                self[key].update(value)
            # elif key == "Hist":
            #     self._history_update(value)
            else:
                self[key] = value

    def diff(self, file):
        diff = copy.deepcopy(self)
        diff.update(file)
        diff = decolorize(diff).splitlines()
        orig = decolorize(self).splitlines()

        color = {' ': '%Reset', '-': '%Red', '+': '%Green', '?': '%Pink'}
        for line in difflib.Differ().compare(orig, diff):
            print(colorize(color[line[0]], line))

    def dump(self, file=None):
        """Dump current session to `file`.
        `file` defaults to self.File if unset.
        """
        if file is None:
            file = self.File

        # get file's absolute path
        file = os.path.truepath(file)

        # if it is a directory, append default session file name
        if os.path.isdir(file):
            file = os.path.truepath(file, SESSION_FILENAME)

        # if file exists and differs from session's binded file,
        # then an user overwriting confirmation is required.
        if os.path.exists(file) and file != self.File:
            question = "File «{}» already exists, overwrite it ?"
            if ui.input.Expect(False)(question.format(file)):
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
            elif object == "Hist":
                self._history_update()
                rawdump[object] = list(self[object])
            else:
                rawdump[object] = rawvar(self[object])

        # write it to the file
        pickle.dump(rawdump, gzip.open(file, 'wb'))


# instanciate main phpsploit session as core.session
session = Session()
