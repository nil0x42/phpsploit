"""
Custom string to append to POST data.

Some TARGET URLs may require specific variables to be set
in POST data (http request message body)

This setting only affects HTTP POST Requests, so you should
set REQ_DEFAULT_METHOD to "POST" for it to take effect.

* EXAMPLE:
# if TARGET url needs alternative POST vars to work properly:
> set REQ_POST_DATA "user=admin&pass=w34kp4ss"

* NOTE:
This setting is useful only to specific cases where TARGET URL
cannot work without it, if you don't need it, or don't know what
you're doing, you should ignore this setting until you need it.
"""
import linebuf


linebuf_type = linebuf.MultiLineBuffer


def validator(value):
    return str(value)


def default_value():
    return ""
