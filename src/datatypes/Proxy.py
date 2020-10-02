"""Proxy tunnel for use through urllib http tunnel. (extends str)
"""
import re
from urllib.request import build_opener, ProxyHandler

import socks
from sockshandler import SocksiPyHandler

from ui.color import colorize


class Proxy(str):
    """Proxy tunnel for use through urllib http tunnel. (extends str)

    Takes None or a proxy in the form <SCHEME>://<HOST>:<PORT>, where scheme
    can be http or https.
    The Proxy datatype returns an urllib opener that includes current
    proxy, or empty opener if the proxy is None.

    Example:
    >>> print(Proxy('127.0.0.1:8080'))
    "http://127.0.0.1:8080"

    """

    _match_regexp = r"^(?:(socks[45]|https?)://)?([\w.-]{3,63})(?::(\d+))$"

    def __new__(cls, proxy=None):
        if str(proxy).lower() == 'none':
            return str.__new__(cls, 'None')

        try:
            components = list(re.match(cls._match_regexp, proxy).groups())
        except:
            synopsis = "[http(s)|socks<4|5>]://<HOST>:<PORT>"
            raise ValueError('Invalid format (must be «%s»)' % synopsis)

        defaults = ['http', '', '']
        for index, elem in enumerate(components):
            if elem is None:
                components[index] = defaults[index]

        proxy = "{}://{}:{}".format(*tuple(components))

        return str.__new__(cls, proxy)

    # pylint: disable=super-init-not-called
    def __init__(self, _=None):
        """Build self._urllib_opener"""

        proxy = super().__str__()

        if proxy == "None":
            self._urllib_opener = build_opener()
            return

        components = list(re.match(self._match_regexp, proxy).groups())
        self.scheme, self.host, self.port = components
        self.components = components

        if self.scheme == "socks4":
            socks4_handler = SocksiPyHandler(socks.PROXY_TYPE_SOCKS4,
                                             self.host,
                                             int(self.port))
            self._urllib_opener = build_opener(socks4_handler)
        elif self.scheme == "socks5":
            socks5_handler = SocksiPyHandler(socks.PROXY_TYPE_SOCKS5,
                                             self.host,
                                             int(self.port))
            self._urllib_opener = build_opener(socks5_handler)
        else:
            proxy_handler = ProxyHandler({'http': proxy, 'https': proxy})
            self._urllib_opener = build_opener(proxy_handler)

    def _raw_value(self):
        return super().__str__()

    def __call__(self):
        return self._urllib_opener

    def __str__(self):
        if not hasattr(self, "scheme"):
            return "None"
        return colorize('%Cyan', self.scheme, '://', '%BoldWhite',
                        self.host, '%BasicCyan', ':', self.port)
