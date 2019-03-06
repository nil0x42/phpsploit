"""Pre-compiled regexes for phpsploit
"""
__all__ = ["WORD_TOKEN"]

import re

# check is given string is a valid phpsploit word token
# usage: WORD_TOKEN.fullmatch("string")
WORD_TOKEN = re.compile("[A-Za-z0-9@_.-]+")
