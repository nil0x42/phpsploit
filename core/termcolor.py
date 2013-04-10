"""Cross-Platform terminal color manager.

"""

import re

def decolorize(string):
    """Remove ANSI color codes from the given string"""
    regex = "\x01?\x1b\[((?:\d|;)*)([a-zA-Z])\x02?"
    return( re.sub(regex, "", string) )


