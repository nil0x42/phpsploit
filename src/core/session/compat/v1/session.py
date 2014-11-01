"""Load a phpsplpoit v1 session file.

This is a backward compatibility component, wich
allows loading phpsploit session files that where
generated with a framework version < 2.1.4.

"""

import pickle
from ..utils import rename_key


def load(path):
    file = open(path, 'rb')
    data = pickle.load(file, encoding="latin1")

    import pprint
    pprint.pprint(data)

    session = {}

    # XXX # File OBJECT ##############################
    session["File"] = None

    # XXX # Alias OBJECT #############################
    session["Alias"] = {}

    # XXX # Cache OBJECT #############################
    session["Cache"] = {}

    # XXX # Hist OBJECT ##############################
    session["Hist"] = {}

    # XXX # Env OBJECT ###############################
    session["Env"] = {}

    # $EDITOR
    rename_key(data["SETTINGS"], "TEXTEDITOR", "EDITOR")
    # $HTTP_USER_AGENT
    rename_key(data["SETTINGS"], "USERAGENT", "HTTP_USER_AGENT")
    if data["SETTINGS"]["HTTP_USER_AGENT"] == "%%RAND_UA%%":
        data["SETTINGS"]["HTTP_USER_AGENT"] = "%%DEFAULT%%"
    # $PASSKEY
    rename_key(data["SETTINGS"], "POSTVAR", "PASSKEY")
    if "%%HASHKEY%%" in data["SETTINGS"]["PASSKEY"]:
        tmp = data["SETTINGS"]["PASSKEY"]
        tmp = tmp.replace("%%HASHKEY%%", data["ENV_HASH"])
        data["SETTINGS"]["PASSKEY"] = tmp
    # $BACKDOOR
    if "%%POSTVAR%%" in data["SETTINGS"]["BACKDOOR"]:
        tmp = data["SETTINGS"]["BACKDOOR"]
        tmp = tmp.replace("%%POSTVAR%%", "%%PASSKEY%%")
        data["SETTINGS"]["BACKDOOR"] = tmp
    # $TARGET
    if "OPENER" in data and "URL" in data["OPENER"]:
        data["SETTINGS"]["TARGET"] = data["OPENER"]["URL"]

    session["Conf"] = data["SETTINGS"]

    return session
