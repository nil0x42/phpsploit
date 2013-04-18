import re
from output import colorize

class Url(str):
    """Http(s) url link. (extends str)

    Takes a string representation of an url link. it must start with
    http(s)://, domain can be an IP address or domain name.

    Example:
    >>> print(Url('google.fr'))
    "http://google.fr:80/"

    """
    _pattern = ('^(?:(https?)?://)?([\w.-]{3,63})'
                '(?::(\d+))?(/.+?)?(?:\?(.+)?)?$')

    _defaults = ['http', '', '80', '/', '']
    def __new__(cls, url):
        try:
            components = list(re.match(cls._pattern, url).groups())
        except:
            raise ValueError('«%s» is not a valid URL Link' %url)

        for index, elem in enumerate(components):
            if elem is None:
                components[index] = cls._defaults[index]

        cls.scheme, cls.host, cls.port, cls.path, cls.query = components
        cls.components = components

        url = "{}://{}:{}{}".format( *tuple(components) )
        if cls.query: url += "?" + cls.query

        return str.__new__(cls, url)


    def __call__(self):
        return super(Url, self).__str__()

    def __str__(self):
        return colorize('%Cyan', self.scheme, '://', '%BoldWhite', self.host,
                        '%BasicCyan', ':', self.port, self.path,
                        ("?"+self.query if self.query else "")               )
