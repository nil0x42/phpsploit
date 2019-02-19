"""
Set max size of POST data allowed in an HTTP request.

This setting is needed to tell phpsploit to generate HTTP
requests that are acceptable for the target server.

* EXAMPLE:
Most http servers allow up to 4MiB per request message body.
Therefore, if the server is configured to only allow up
to 300KiB, phpsploit could fail to execute payloads
unless you change value of REQ_MAX_HEADERS to 300 KiB:
> set REQ_MAX_HEADERS 300KiB

* NOTE:
If you encounter http error 500 or if payload execution fails,
you may need to lower the default limit of this setting.

* REFERENCES:
http://httpd.apache.org/docs/2.2/mod/core.html#LimitRequestBody
https://secure.php.net/manual/en/ini.core.php#ini.post-max-size
"""
import linebuf
import datatypes


linebuf_type = linebuf.RandLineBuffer

def validator(value):
    value = datatypes.ByteSize(value)
    if 250 > value:
        raise ValueError("can't be less than 250 bytes")
    return value


def default_value():
    return "4 MiB"
