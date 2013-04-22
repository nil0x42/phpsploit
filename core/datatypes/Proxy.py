import re
from ui.color import colorize
from urllib.request import build_opener, ProxyHandler

#TODO: add support for socks4://, socks://, socks5:// proxy types
# it can be done with this lib: https://gist.github.com/e000/869791
# or traditionnally by changing the default socket.

class Proxy(str):
    """Proxy tunnel for use through urllib http tunnel. (extends str)

    Takes None or a proxy in the form <SCHEME>://<HOST>:<PORT>, where scheme
    can be http or https.
    The Proxy datatype returns an urllib opener that includes current
    proxy, or empty opener is the proxy is None.

    Example:
    >>> print(Proxy('127.0.0.1:8080'))
    "http://127.0.0.1:8080"

    """


    # commented out because no socks support for the moment
    #_synopsis = "[http(s)|socks<4|5>]://<HOST>:<PORT>"
    #_pattern  = "^(?:(socks[45]|https?)?://)?([\w.-]{3,63})(?::(\d+))$"

    _synopsis = "http(s)://<HOST>:<PORT>"
    _pattern  = "^(?:(https?)://)?([\w.-]{3,63})(?::(\d+))$"
    _defaults = ['http', '', '']

    def __new__(cls, proxy):
        cls._urllib_opener = build_opener()
        if str(proxy).lower() == 'none':
            return str.__new__(cls, 'None')

        try:
            components = list(re.match(cls._pattern, proxy).groups())
        except:
            raise ValueError('Invalid format (must be «%s»)' %cls._synopsis)

        for index, elem in enumerate(components):
            if elem is None:
                components[index] = cls._defaults[index]

        cls.scheme, cls.host, cls.port = components
        cls.components = components

        proxy = "{}://{}:{}".format( *tuple(components) )

        proxy_handler = ProxyHandler( {'http':proxy, 'https':proxy} )
        cls._urllib_opener.add_handler( proxy_handler )

        return str.__new__(cls, proxy)


    def __raw_value(self):
        return super(Proxy, self).__str__()


    def __call__(self):
        return self._urllib_opener


    def __str__(self):
        return colorize('%Cyan', self.scheme, '://', '%BoldWhite',
                        self.host, '%BasicCyan', ':', self.port)
