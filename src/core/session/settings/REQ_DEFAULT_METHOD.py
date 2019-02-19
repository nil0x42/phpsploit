"""
Default HTTP method to use to communicate with TARGET.

The phpsploit framework supports both GET and POST methods
to send HTTP requests

* GET METHOD:
-------------
# BEHAVIOR:
    The PASSKEY payload stager is passed as a single HTTP header,
    and a set of HTTP headers are created, and fullfilled with
    a portion of the payload, respecting limitations imposed
    by REQ_MAX_HEADERS and REQ_MAX_HEADER_SIZE settings.
# PROS:
    This method is usually the stealthiest one, as common log
    analysis softwares don't analyse HTTP Headers at all.
# CONS:
    The amount of data that can be injected is limited by remote
    server's REQ_MAX_HEADERS and REQ_MAX_HEADER_SIZE.
    So phpsploit may need to run multi-request payloads more
    frequently.

* POST METHOD:
--------------
# BEHAVIOR:
    The PASSKEY payload stager is passed as a single HTTP header,
    and the final payload is sent as a big POSTDATA argument
    (named with PASSKEY), respecting limitations imposed
    by REQ_MAX_POST_SIZE setting.
# PROS:
    Remote server's REQ_MAX_POST_SIZE has generally a large value,
    So big payloads can be sent through a single HTTP request,
    instead of sending a lot of GET multi-requests.
# CONS:
    Triggering a lot of POST requests on TARGET url can raise
    suspicion, as this kind of request is not expected on
    most of URLs.
"""
import linebuf


linebuf_type = linebuf.RandLineBuffer


def validator(value):
    value = value.upper()
    if value not in ["GET", "POST"]:
        raise ValueError("available methods: GET/POST")
    return value


def default_value():
    return "GET"
