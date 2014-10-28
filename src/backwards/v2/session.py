"""Load a phpsplpoit v2 session file.

This is a backward compatibility component, wich
allows loading phpsploit session files that where
generated with a framework version between versions
2.0.0Alpha and 2.1.4.

"""

import pickle
from backwards.utils import rename_key, remove_key


def load(path):
    """Loads `file` as a deprecated pickled PhpSploit session file.

    """
    file = open(path, 'rb')
    data = pickle.load(file, encoding="latin1")

    # only phpsploit 2 < 2.2 sessions are supported
    assert data["PSCOREVER"] == 2

    session = {}

    # XXX # File OBJECT ##############################
    session["File"] = None

    # XXX # Alias OBJECT #############################
    session["Alias"] = {}

    # XXX # Cache OBJECT #############################
    session["Cache"] = {}

    # XXX # Hist OBJECT ##############################
    session["Hist"] = {}

    # XXX # Conf OBJECT ##############################
    # if useragent is an old default, remove it
    oldDefaultUA = ["file://misc/http/User-Agent.lst",
                    "file://framework/misc/http_user_agents.lst"]
    if "HTTP_USER_AGENT" in data["SET"].keys() \
            and data["SET"]["HTTP_USER_AGENT"] in oldDefaultUA:
        del data["SET"]["HTTP_USER_AGENT"]
    # remove SAVEFILE
    remove_key(data["SET"], "SAVEFILE")
    # bind settings
    session["Conf"] = data["SET"]

    # XXX # Env OBJECT ###############################
    rename_key(data["ENV"], "CWD", "PWD")
    rename_key(data["ENV"], "WRITE_TMPDIR", "WRITEABLE_TMPDIR")
    rename_key(data["ENV"], "WRITE_WEBDIR", "WRITEABLE_WEBDIR")

    remove_key(data["ENV"], "TEXTEDITOR")
    # bind environment vars
    session["Env"] = data["ENV"]
    # add some env vars from old SRV object:
    session["Env"]["ADDR"] = data["SRV"]["addr"]
    session["Env"]["HOME"] = data["SRV"]["home"]
    session["Env"]["HOST"] = data["SRV"]["host"]
    session["Env"]["PHP_VERSION"] = data["SRV"]["phpver"]
    session["Env"]["PATH_SEP"] = data["SRV"]["separator"]
    session["Env"]["HTTP_SOFTWARE"] = data["SRV"]["soft"]
    session["Env"]["USER"] = data["SRV"]["user"]
    session["Env"]["WEB_ROOT"] = data["SRV"]["webroot"]
    session["Env"]["PORT"] = data["SRV"]["port"]
    session["Env"]["CLIENT_ADDR"] = data["SRV"]["client_addr"]

    # determine PLATFORM (one word, lowercase)
    session["Env"]["PLATFORM"] = data["SRV"]["os"].split()[0].lower()
    if session["Env"]["PLATFORM"] == "unknow":
        if session["Env"]["PATH_SEP"] == "\\":
            session["Env"]["PLATFORM"] = "windows"
        else:
            session["Env"]["PLATFORM"] = "unix"

    rename_key(session["Conf"], "TEXTEDITOR", "EDITOR")
    rename_key(session["Conf"], "WEBBROWSER", "BROWSER")

    return session
