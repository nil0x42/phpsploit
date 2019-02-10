"""
Use a proxy to connect to the target

You can set a proxy in order to encapsulate the whole phpsploit
requests for furtivity or network analysis purposes.

This setting supports HTTP, HTTPS, SOCKS4
and SOCKS5 proxy schemes.

PROXY SYNTAX: <SCHEME>://<ADDRESS>:<PORT>

* EXAMPLES:

# To unset PROXY, set it's value to 'None' magic string:
> set PROXY None

# To set a socks5 proxy to connect through Tor:
> set PROXY socks5://127.0.0.1:9050
"""
import linebuf
import datatypes


linebuf_type = linebuf.RandLineBuffer


def validator(value):
    return datatypes.Proxy(value)


def default_value():
    return None
