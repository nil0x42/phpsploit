"""Cross-Platform terminal color manager.

"""

import re
import colorama, colorama_patched


ANSI_CODES = {"RESET"       : 0,
              "BOLD"        : 1,
              "DIM"         : 2,
              "UNDERLINE"   : 4,
              "BLINK"       : 5,
              "REVERT"      : 7,
              "NORMAL"      : 22,

              "black"       : 30,
              "red"         : 31,
              "green"       : 32,
              "yellow"      : 33,
              "blue"        : 34,
              "magenta"     : 35,
              "cyan"        : 36,
              "white"       : 37,
              "default"     : 39}



def draw(ansiCodes):
    """Takes a comma separated list of color codes, and return
    the corresponding ansi color codes.

    """
    result = ""
    for code in ansiCodes.split(','):
        result += "\x1b[%dm" %ANSI_CODES[code]
    return(result)


def format(string):
    """Takes a color formated string as argument, and return
    it's ANSI colored version.

    """
    patterns = "\%\{([A-Za-z,]+?)\}"
    return( re.sub(patterns, draw, string) )


def blank(string):
    """Remove ANSI color codes from the given string"""
    regex = "\x01?\x1b\[((?:\d|;)*)([a-zA-Z])\x02?"
    return( re.sub(regex, "", string) )


