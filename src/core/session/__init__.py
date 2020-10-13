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
    * Hist  -> Readline history
"""
import os
import re
import gzip
import pickle
import difflib

import metadict
import utils.path
import ui.input
from ui.color import colorize, decolorize
from core import encoding

from . import settings
from . import environment
from . import history
from . import compat_session

SESSION_FILENAME = "phpsploit.session"


class Session(metadict.MetaDict):
    """Phpsploit Session
    """

    # pylint: disable=invalid-name
    def __init__(self):
        """Instanciate the phpsploit session.
        It handles settings, environment variables, aliases
        and readline history (if readline is available).
        """
        # process parent class init
        super().__init__()

        # session objects declaration
        self.Conf = settings.Settings()
        self.Env = {}
        self.Alias = metadict.VarContainer(title="Command Aliases")
        self.Hist = history.History()
        self.Compat = {}
        self.File = None

    @staticmethod
    def _isattr(name):
        """Session items are alphabetic and capitalized strings"""
        return re.match("^[A-Z][a-z]+$", name)

    def _history_update(self, array=None):
        if array is None:
            array = []
        try:
            import readline
            # add array elements to readline history
            for command in array:
                readline.add_history(command)
            # recreate Hist from readline history (UGLY)
            self.Hist.clear()
            history_len = readline.get_current_history_length()
            for i in range(1, history_len + 1):
                line = readline.get_history_item(i)
                self.Hist.append(line)
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
                # pylint: disable=not-callable
                value = self.Conf.SAVEPATH() + SESSION_FILENAME
            elif not os.path.isdir(value) and os.sep not in value:
                # pylint: disable=not-callable
                value = self.Conf.SAVEPATH() + value
        return value

    def __setitem__(self, name, value):
        if name == "Env":
            # Assuming that value can be set as a dict(),
            # we use special wrapper for setting value
            # as an Environment() instance.
            value = environment.Environment(value)
        super().__setitem__(name, value)

    def __str__(self):
        """Get a nice string representation of current session
        """
        title = "PhpSploit session dump ({})".format(self.File)
        # deco = "\n" + colorize("%Blue", "=" * len(title)) + "\n"
        deco = "\n" + colorize("%Blue", "=" * 68) + "\n"
        data = deco + title + deco
        ordered_keys = ["Conf", "Env", "Alias"]
        for name in ordered_keys:
            if self[name]:
                data += str(self[name]) + "\n"
        return data

    def __call__(self, file=None, fatal_errors=True):
        """Load and return the session object stored in `file`.
        if `file` is None, current session (self) is returned.

        """
        # A None/empty call returns current session as it is
        if file is None:
            return self
        file = utils.path.truepath(file)
        # append default filename if is a directory
        if os.path.isdir(file):
            file = utils.path.truepath(file, SESSION_FILENAME)
        # get unpickled `data` from `file`
        try:
            data = pickle.load(gzip.open(file),
                               encoding=encoding.default_encoding,
                               errors=encoding.default_errors)
            if "Compat" not in data.keys():
                data["Compat"] = {}
        except OSError as error:
            if "not a gzipped file" in str(error).lower():
                data = compat_session.load(file)
                if not data:
                    raise ValueError("Not a phpsploit session file")
            else:
                raise
        # get Session() obj from raw session value
        sess = self._obj_value(data, fatal_errors=fatal_errors)
        # bind new session's File to current file
        sess.File = file
        return sess

    def load(self, file=None, fatal_errors=True):
        """get a new Session() loaded from `file`
        """
        return self(file, fatal_errors=fatal_errors)

    # pylint: disable=arguments-differ
    def update(self, obj=None, update_history=False):
        """Update current session with `obj`.
        The given argument can be a dictionnary instance, in which case
        it must be a valid session object to merge in.
        If `obj` is a string, it is then considered as a file path, and
        the self __call__() method is then used in order to retrieve
        corresponding session object.
        Is `obj` is None (default), "${SAVEPATH}./phpsploit.session" is used.

        """
        file = None
        if isinstance(obj, str):
            file = obj
            obj = self.load(file)
        elif obj is None:
            file = self.File
            obj = self.load(file)
        # if obj is not a dict instance, fallback to parent method
        elif not isinstance(obj, dict):
            super().update(obj)
            return

        for key, value in obj.items():
            if key == "Compat":
                self[key] = value
            elif isinstance(self[key], dict):
                self[key].update(value)
            elif key == "Hist":
                if update_history and file is not None:
                    self._history_update(value)
            else:
                self[key] = value

    def deepcopy(self, target=None):
        """Create a deep copy of current session
        All contained objects are recursively guaranted to be duplicated
        """
        if target is None:
            target = self
        return self._obj_value(self._raw_value(target))

    def diff(self, file=None, display_diff=False):
        """This function returns True is the given `file` is
        a phpsploit session which differs from current session.
        Otherwise, False is returned.

        Additionally, if `display_diff` is set, the session
        differences will be displayed in common unix `diff` style.
        """
        if isinstance(file, Session):
            diff = self.deepcopy(file)
        else:
            if file is None:
                diff = Session()
                diff.File = self.File
            else:
                diff = self.deepcopy()
            diff.update(file)

        diff = decolorize(diff).splitlines()
        orig = decolorize(self).splitlines()

        if display_diff:
            color = {' ': '%Reset', '-': '%Red', '+': '%Green', '?': '%Pink'}
            if file is None:
                difflines = difflib.Differ().compare(diff, orig)
            else:
                difflines = difflib.Differ().compare(orig, diff)
            for line in difflines:
                # dont be too much verbose...
                if line.startswith('?'):
                    continue
                print(colorize(color[line[0]], line))

        return diff != orig

    def _raw_value(self, sess=None):
        """Get a 'built-in types only' representation of `sess`
        Session() object.

        This @staticmethod is guaranted to return only python built-in
        types, and is therefore useful to dump Session() in a stable state.

        To restore a raw value, use _obj_value() method.

        >>> from core import session
        >>> type(session)
        <class 'core.session.Session'>
        >>> raw = session._raw_value(session)
        >>> type(raw)
        <class 'dict'>
        """
        if sess is None:
            sess = self
        rawdump = {}
        for obj in sess.keys():
            rawdump[obj] = {}
            rawvar = (tuple if obj == "Conf" else str)
            if isinstance(sess[obj], dict):
                for var, value in sess[obj].items():
                    rawdump[obj][var] = rawvar(value)
                if obj == "Env":
                    # HACK: store env defaults as __DEFAULTS__
                    rawdump["Env"]["__DEFAULTS__"] = sess["Env"].defaults
            elif obj == "Hist":
                rawdump["Hist"] = list(sess["Hist"])
            else:
                rawdump[obj] = rawvar(sess[obj])
        return rawdump

    def _obj_value(self, raw=None, fatal_errors=True):
        """Restore Session() from its 'built-in types only' representation.
        Used to get back Session() from data returned by _raw_value() method

        >>> from core import session
        >>> raw = session._raw_value(session)
        >>> type(raw)
        <class 'dict'>
        >>> restored = session._obj_value(raw)
        >>> type(restored)
        <class 'core.session.Session'>
        """
        def update_obj(obj, new, fatal_errors=True):
            elems = list(obj.keys())
            if "Conf" in elems:
                elems.remove("Conf")
                elems.insert(0, "Conf")
            if "Env" in elems:
                elems.remove("Env")
                obj["Env"].update(new["Env"])
            if "Hist" in elems:
                elems.remove("Hist")
                obj["Hist"] += new["Hist"]
            for elem in elems:
                if isinstance(obj[elem], dict):
                    for key, value in new[elem].items():
                        try:
                            obj[elem][key] = value
                        except Exception as error:
                            item_repr = "session.%s.%s" % (elem, key)
                            msg_prefix = "[-] Couldn't set %s" % item_repr
                            if fatal_errors:
                                print("%s:" % msg_prefix)
                                raise
                            else:
                                print("%s: %s" % (msg_prefix, error))
                else:
                    obj[elem] = new[elem]
            return obj
        obj = Session()
        obj = update_obj(obj, self._raw_value(self))
        if raw is not None:
            if raw.keys() != obj.keys():
                raise ValueError("Invalid raw session")
            obj = update_obj(obj, raw, fatal_errors=False)
        return obj

    def dump(self, file=None, ask_confirmation=True):
        """Dump current session to `file`.
        `file` defaults to self.File if unset.
        """
        if file is None:
            file = self.File

        # get file's absolute path
        file = utils.path.truepath(file)

        # if it is a directory, append default session file name
        if os.path.isdir(file):
            file = utils.path.truepath(file, SESSION_FILENAME)

        # if file exists and differs from session's binded file,
        # then an user overwriting confirmation is required.
        if ask_confirmation and os.path.exists(file):
            if file != self.File or super().__getitem__("File") is None:
                question = "File «{}» already exists, overwrite it ?"
                if ui.input.Expect(False)(question.format(file)):
                    raise Warning("The session was not saved")

        # write it to the file
        self._history_update()
        raw = self._raw_value(self)
        pickle.dump(raw, gzip.open(file, 'wb'))


# instanciate main phpsploit session as core.session
session = Session()
