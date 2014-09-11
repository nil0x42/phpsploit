"""
A password like backdoor protection setting.

This passkey is used by the $BACKDOOR setting
and phpsploit's http tunneling mechanisms as
the mains dynamic payload dispatcher, based on
a special header.

While exploiting a phpsploit remote TARGET, this
setting must have the same value than the one
used when the remote backdoor was set.

Indeed, permanently changing the $PASSKEY value
from the default one to another value of your choice
ensures that other phpsploit users will not be able
to connect to your personnal backdoors without
knowlege of your $PASSKEY.

Permanent change of the PASSKEY's default value is
then highly recommended. This can be done by adding
'set PASSKEY <yourPasskey>' to the phpsploit
configuration file.
"""
import re

import objects


type = objects.buffers.MultiLineBuffer


def setter(value):
    value = str(value).lower()
    reserved_headers = ['host', 'accept-encoding', 'connection',
                        'user-agent', 'content-type', 'content-length']
    if not value:
        raise ValueError("can't be an empty string")
    if not re.match("^[a-zA-Z0-9_]+$", value):
        raise ValueError("only chars from set «a-Z0-9_» are allowed")
    if re.match('^zz[a-z]{2}$', value) or \
       value.replace('_', '-') in reserved_headers:
        raise ValueError("reserved header name: «{}»".format(value))
    return value


def default_value():
    raw_value = "phpSpl01t"
    return setter(raw_value)
