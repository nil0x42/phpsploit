"""
The string defined here will be appended
to POST data when REQ_DEFAULT_METHOD is POST.

E.g:
    set REQ_DEFAULT_METHOD "POST"
    set REQ_POST_DATA "var1=value1&var2=value2"
"""
import objects
import datatypes


type = objects.buffers.MultiLineBuffer


def setter(value):
    return str(value)


def default_value():
    return ""
