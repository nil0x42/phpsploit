"""String functions

Author: nil0x42
"""


def isgraph(string):
    """Check if string contains only printable characters except space
    """
    for char in string:
        if not 0x21 <= ord(char) <= 0x7E:
            return False
    return True
