"""Terminal color and style manager. (made for PhpSploit)

"""

import re
import colorama, colorama_patched


ANSI_CODES = {# styling codes
              "RESET"       : 0,
              "BRIGHT"      : 1,
              "DIM"         : 2,
              "ITALIC"      : 3,
              "UNDERLINE"   : 4,
              "BLINK"       : 5,
              "REVERT"      : 7,
              "NORMAL"      : 22,
              # coloration codes
              "black"       : 30,
              "red"         : 31,
              "green"       : 32,
              "yellow"      : 33,
              "blue"        : 34,
              "magenta"     : 35,
              "cyan"        : 36,
              "white"       : 37,
              "default"     : 39}



def draw(codes):
    """Draw the given ansi color list (which may be a string or
    SRE_MATCH object).
    They must be comma separated, and each element is picked from
    the ANSI_CODES dictionnary.

    >>> termcolor.draw('DIM,red')
    '\\x1b[2m\\x1b[31m'
    """
    if not isinstance(codes, str):
        try: codes = codes.group(1)
        except: raise ValueError("Invalid color list: {}".format(codes))
    result = ""
    for code in codes.split(','):
        try: result += "\x1b[%dm" %ANSI_CODES[code]
        except: pass
    return result


def format(string):
    """Format the given string, converting ~{ANSI,CODES} sequences
    with the draw() function.
    >>> termcolor.format('~{DIM,green}colored string~{RESET}')
    '\\x1b[2m\\x1b[32mcolored string\\x1b[0m'
    """
    patterns = "\~\{([A-Za-z,]+?)\}"
    return re.sub(patterns, draw, string)


def blank(string):
    """Remove ANSI color/style codes from the given string.

    >>> termcolor.blank('string \\x1b[2m\\x1b[32mcolor !\\x1b[0m')
    'string color !'
    """
    regex = "\x01?\x1b\[((?:\d|;)*)([a-zA-Z])\x02?"
    return re.sub(regex, "", string)
