"""
The interval in seconds to sleep between two
http requests.

This request configuration setting is used
while sending a multipart http requests in cases
where the payload is larger than available space
in a single request.
Indeed, this setting forces the requests engine
to sleep a random number of seconds between the
given interval.

Setting it to an high value can help furtivity
while sending a very large payload, for example
when you are uploading a very big file to the
remote server whith the `upload` plugin.
"""
import objects
import datatypes


type = objects.buffers.RandLineBuffer


def setter(value):
    return datatypes.Interval(value)


def default_value():
    raw_value = "1-10"
    return setter(raw_value)
