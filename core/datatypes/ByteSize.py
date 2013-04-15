import termcolor

class ByteSize(int):
    """Human readable byte size representation. (extends int)

    Extends: int

    The ByteSize datatype takes a string which represents an human
    easy to type byte number. It also accepts integers as argument,
    in which case the raw value is kept as it is.

    Example:
    >>> size = ByteSize("1 kb")
    >>> size()
    1024
    >>> print(size)
    1 KiB (1024 bytes)

    NOTE: The input parser is very (too much ?) flexible, it accepts
    as input value any string representing a float or int, followed by
    one of the byte metrics first letters, aka "K", "M", "G" and "T".
    Otherwise, the number must be alone or followed by "O" or "B", which
    means that the number represent a non multipliable value.
    Conclusion: "200BITCOINS" will be accepted as a 200 Bytes value, and
    "3 Thousands", considered as 3 Terabytes...

    """
    _metrics = 'BKMGT' # ordered byte metric prefixes

    def __new__(cls, value=0):

        # convert to an uppercase string, and format it.
        value = str(value).replace(',', '.').upper() + 'B'
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
        multiplier = 1024 ** ( cls._metrics.find(metric) )
        result = int( number * multiplier )

        return int.__new__(cls, result)


    def __call__(self):
        return int(self)


    def __str__(self):
        self_str = super(ByteSize, self).__str__()
        if self == 1:
            return "1 byte"

        number = float( self )

        for index in range( len(self._metrics) ):
            if number < 1024.0 \
            or index == len(self._metrics)-1:
                break
            number /= 1024.0

        intLen = len(str( int(number) ))
        precision = max( 0 , 3-intLen )
        number = str( round(number, precision) ).rstrip('0').rstrip('.')

        byteNames = ('bytes', 'KiB', 'MiB', 'GiB', 'TiB')
        result = number + " " + byteNames[index]
        if index > 0:
            result += termcolor.draw('DIM,ITALIC,white')
            result += " (%s bytes)" %self_str
            result += termcolor.draw('RESET')
        return result

