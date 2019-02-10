"""
Set the maximum phpsploit session file size.

While using the phpsploit framework, some usage informations
are stored, such as commands history.
Changing this limit ensures that the session, if saved whith
`session save` command will not exceed a certain size.

* USE CASES:
phpsploit's history uses this value to determine the maximum
number of command lines to store in session file.
"""
import linebuf
import datatypes

linebuf_type = linebuf.MultiLineBuffer


def validator(value):
    return datatypes.ByteSize(value)


def default_value():
    return "1 MiB"
