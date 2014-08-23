import objects
import datatypes


class PROXY:
    """
    The proxy to use for request encapsulation.

    You can set a proxy in order to encapsulate
    the whole phpsploit requests for furtivity
    or network analysis purposes.

    This setting supports HTTP, HTTPS, SOCKS4
    and SOCKS5 proxy types.

    PROXY SYNTAX: <SCHEME>://<ADDRESS>:<PORT>
    """
    type = objects.settings.RandLineBuffer

    def setter(self, value):
        return datatypes.Proxy(value)

    def default_value(self):
        return self.setter(None)
