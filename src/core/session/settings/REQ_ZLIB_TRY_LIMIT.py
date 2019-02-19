"""
Control over which payload size the zlib compression feature
will be disabled.

The phpsploit request engine does'its best to compress and fit
the payload within as little HTTP Requests as possible.

Therefore, zlib compression becomes exponentially CPU greedy
as payload size gows up, and it might be extremelly slow to
process very large requests.

The REQ_ZLIB_TRY_LIMIT defines a value over which the payload
is no more processed by zlib compression. Payloads over this
value will then be encoded without zlib compression, making them
bigger, but also a lot faster to generate.
"""
import linebuf
import datatypes


linebuf_type = linebuf.RandLineBuffer


def validator(value):
    value = datatypes.ByteSize(value)
    if value < 1:
        raise ValueError("must be a positive bytes number")
    return value


def default_value():
    return "20 MiB"
