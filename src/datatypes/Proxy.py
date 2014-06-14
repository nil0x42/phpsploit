import re
import http
import urllib
from urllib.request import build_opener, ProxyHandler

import socks

from ui.color import colorize


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

    _match_regexp = "^(?:(socks[45]|https?)://)?([\w.-]{3,63})(?::(\d+))$"

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

    def __init__(self, _=None):
        """Build self._urllib_opener"""

        proxy = super().__str__()
        self._urllib_opener = build_opener()

        if proxy == "None":
            return

        components = list(re.match(self._match_regexp, proxy).groups())
        self.scheme, self.host, self.port = components
        self.components = components

        if self.scheme == "socks4":
            handler = SocksiPyHandler(socks.PROXY_TYPE_SOCKS4,
                                      self.host,
                                      int(self.port))
        elif self.scheme == "socks5":
            handler = SocksiPyHandler(socks.PROXY_TYPE_SOCKS5,
                                      self.host,
                                      int(self.port))
        else:
            handler = ProxyHandler({'http': proxy, 'https': proxy})

        self._urllib_opener.add_handler(handler)

    def _raw_value(self):
        return super().__str__()

    def __call__(self):
        return self._urllib_opener

    def __str__(self):
        if not hasattr(self, "scheme"):
            return "None"
        return colorize('%Cyan', self.scheme, '://', '%BoldWhite',
                        self.host, '%BasicCyan', ':', self.port)


class SocksiPyConnection(http.client.HTTPConnection):
    def __init__(self, version, addr, port=None, rdns=True,
                 username=None, password=None, *args, **kwargs):
        self.proxyargs = (version, addr, port, rdns, username, password)
        http.client.HTTPConnection.__init__(self, *args, **kwargs)

    def connect(self):
        self.sock = socks.socksocket()
        self.sock.setproxy(*self.proxyargs)
        if isinstance(self.timeout, float):
            self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))


class SocksiPyHandler(urllib.request.HTTPHandler):
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kw = kwargs
        urllib.request.HTTPHandler.__init__(self)

    def http_open(self, req):
        def build(host, port=None, strict=None, timeout=0):
            con = SocksiPyConnection(*self.args, host=host, port=port,
                                     strict=strict, timeout=timeout, **self.kw)
            return con

        return self.do_open(build, req)
