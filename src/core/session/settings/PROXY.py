"""
The proxy to use for request encapsulation.

You can set a proxy in order to encapsulate
the whole phpsploit requests for furtivity
or network analysis purposes.

This setting supports HTTP, HTTPS, SOCKS4
and SOCKS5 proxy types.

PROXY SYNTAX: <SCHEME>://<ADDRESS>:<PORT>
"""
import objects
import datatypes


type = objects.buffers.RandLineBuffer


def setter(value):
    return datatypes.Proxy(value)


def default_value():
    return setter(None)
