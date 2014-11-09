"""Generic encoding handler.

This small string encoding/decoding manager aims to provide
an uniform encoding handling policy for the phpsploit framework.
"""

import sys
import codecs


try:
    codecs.lookup("utf-8")
    default_encoding = "utf-8"
except LookupError:
    default_encoding = sys.getdefaultencoding()

try:
    codecs.lookup_error("surrogateescape")
    default_errors = "surrogateescape"
except LookupError:
    default_errors = "strict"


def encode(str_obj, encoding=default_encoding, errors=default_errors):
    """Encode the given bytes object with `encoding` encoder
    and `errors` error handler.
    If not set, `encoding` defaults to module's `default_encoding` variable.
    If not set, `errors` defaults to module's `default_errors` variable.
    """
    bytes_obj = str_obj.encode(encoding, errors)
    return bytes_obj


def decode(bytes_obj, encoding=default_encoding, errors=default_errors):
    """Decode the given bytes object with `encoding` decoder
    and `errors` error handler.
    If not set, `encoding` defaults to module's `default_encoding` variable.
    If not set, `errors` defaults to module's `default_errors` variable.
    """
    str_obj = bytes_obj.decode(encoding, errors)
    return str_obj
