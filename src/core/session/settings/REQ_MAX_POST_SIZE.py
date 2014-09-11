"""
This setting defines maximum size of
the post data per http request to the
target server.

Most http servers allow up to 4MB for
post data, therefore, if the server
administrator have configured it to a lower
limit, execution of requests can fail and
lead to an http error 500 or something else.
"""
import objects
import datatypes


type = objects.buffers.RandLineBuffer


def setter(value):
    value = datatypes.ByteSize(value)
    if 250 > value:
        raise ValueError("can't be less than 250 bytes")
    return value


def default_value():
    raw_value = "4 MiB"
    return setter(raw_value)
