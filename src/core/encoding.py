"""Generic encoding handler.

This small string encoding/decoding manager aims to provide
an uniform encoding handling policy for the phpsploit framework.
"""

import codecs


default_encoding = ""
default_errors = ""


def encode(str_obj, encoding="", errors=""):
    """Encode the given bytes object with `encoding` encoder
    and `errors` error handler.
    If not set, `encoding` defaults to module's `default_encoding` variable.
    If not set, `errors` defaults to module's `default_errors` variable.
    """
    if not encoding:
        encoding = default_encoding
    if not errors:
        errors = default_errors
    bytes_obj = str_obj.decode(encoding, errors)
    return bytes_obj


def decode(bytes_obj, encoding="", errors=""):
    """Decode the given bytes object with `encoding` decoder
    and `errors` error handler.
    If not set, `encoding` defaults to module's `default_encoding` variable.
    If not set, `errors` defaults to module's `default_errors` variable.
    """
    if not encoding:
        encoding = default_encoding
    if not errors:
        errors = default_errors
    str_obj = bytes_obj.decode(encoding, errors)
    return str_obj


def set_default_encoding(*args):
    """Takes n candidates to be used as default encoding
    and choose the first one which is available.
    If no candidate is available, default_encoding is set to 'utf-8'.
    """
    global default_encoding
    default_encoding = "utf-8"
    for candidate in args:
        try:
            codecs.lookup(candidate)
        except LookupError:
            continue
        default_encoding = candidate
        break


def set_default_errors(*args):
    """Takes n candidates to be used as default error handlers
    and choose the first one which is available.
    If no candidate is available, default_errors is set to 'strict'.
    """
    global default_errors
    default_errors = "strict"
    for candidate in args:
        try:
            codecs.lookup_error(candidate)
        except LookupError:
            continue
        default_errors = candidate
        break


# initialize default_encoding to 'utf-8'
set_default_encoding("utf-8")

# initialise default_errors to 'surrogateescape'
# is not available, default to 'strict' error handler.
set_default_errors("surrogateescape", "strict")
