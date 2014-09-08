"""
Default HTTP method to use in requests.

The phpsploit framework supports both GET
and POST methods for sending HTTP requests.

GET METHOD:
-----------
  MODUS OPERANDI:
    The $PASSKEY payload launcher is passed as a
    single header, and all other available headers
    are fullfilled in a fragmented manner with
    the obfuscated php payload according to
    $HTTP_MAX_HEADERS and $HTTP_MAX_HEADER_SIZE
    settings limitations.
  DESCRIPTION:
    This method is usually more stealth than
    POST, because most of HTTP requests in
    the web use the GET method.
    Therefore, the amount of payload that can
    be injected in a single request is generally
    limited by remote web server's maximum headers
    and maximum size of each header.
POST METHOD:
------------
  MODUS OPERANDI:
    The $PASSKEY payload launcher is passed as a
    single header, and the php payload is sent
    through a POST argument, according to
    $HTTP_MAX_POST_SIZE settings limitations.
  DESCRIPTION:
    Choosing this method is usually interesting
    when sending a large payload wich otherwise
    needs the sending of a lot more GET requests.
    Using this method can also be useful when the
    target is usually called with post requests for
    stealth purposes, but this is rarely the case.
"""
import objects


type = objects.settings.RandLineBuffer


def setter(value):
    value = value.upper()
    if value not in ["GET", "POST"]:
        raise ValueError("available methods: GET/POST")
    return value


def default_value():
    raw_value = "GET"
    return setter(raw_value)
