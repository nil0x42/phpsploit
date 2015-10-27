from ui.color import colorize


class ByteSize(int):
    """Human readable byte size representation. (extends int)

    Takes an integer or byte number string representation (e.g. "1kb").

    >>> size = ByteSize("1 KB")
    >>> print(size)
    1 KiB (1024 bytes)
    >>> size()
    1024

    """
    _metrics = 'BKMGT'  # ordered byte metric prefixes

    def __new__(cls, value=0):

        # convert to an uppercase string, and format it.
        value = str(value)
        if len(value.splitlines()) != 1:
            raise ValueError("invalid byte size representation")

        value = value.replace(',', '.').upper() + 'B'
        value = value.replace(' ', '').replace('O', 'B')

        # get back float number and metric prefix
        number = metric = str()
        for char in value:
            if char in '0123456789.':
                number += char
            else:
                metric = char
                break

        # make sure the syntax is correct
        try:
            number = float(number)
            assert metric in cls._metrics
        except:
            raise ValueError("invalid byte size representation")

        # get the real integer value, and return it's int instance
        multiplier = 1024 ** (cls._metrics.find(metric))
        result = int(number * multiplier)

        return int.__new__(cls, result)

    def _raw_value(self):
        return int(self)

    def __call__(self):
        return self._raw_value()

    def __str__(self):
        self_str = super().__str__()
        if self == 1:
            return "1 byte"

        number = float(self)

        for index in range(len(self._metrics)):
            if number < 1024.0 or index == len(self._metrics)-1:
                break
            number /= 1024.0

        intLen = len(str(int(number)))
        precision = max(0, (3 - intLen))
        number = str(round(number, precision)).rstrip('0').rstrip('.')

        byteNames = ('bytes', 'KiB', 'MiB', 'GiB', 'TiB')
        result = number + " " + byteNames[index]
        if index > 0:
            result += colorize(" ", '%DimWhite', "(%s bytes)" % self_str)

        return result
