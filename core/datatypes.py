"""
This is a Py2.7 collection of data types especially customized for the
PhpSploit framework. They are prefered as variable types for PhpSploit
settings and environment variables, instead of the python built-in
data types, such as str(), int(), list(), etc...

Data type classes handles at least the following method calls:
* obj.__call__() <==> obj()
    Return the current data value, in the object's base data type.

* obj.__repr__() <==> repr(obj)
    Return a nice string representation of the object, as it must be
    displayed on the terminal.

Example:

>>> import datatype
>>> maxSize = datatype.ByteSum('2ko')
>>> repr(maxSize)
'2KiB'
>>> maxSize()
2048
>>>
>>> interval = datatype.NumRange('2-5')
>>> repr(interval)
'range(2,5)'
>>> interval()
2.2
>>> interval()
4.99
>>> interval()
3.11
>>> interval()
1.01

todo:
ByteSize -> an human metric byte size representation (extends int)
PhpCode  -> a php code string (extends str)
RandLine -> a random line from multiline string (extends list or str ???)
Interval -> a random interval between two floats (extends tuple ???)
Proxy    -> an urllib opener instance from string (extends str)
Url      -> an http(s) url link
Path     -> ???


the datatypes can include also a coloration on the __repr__ to interract with
a future hypothetical overload of sys.stdout, for example PhpCode's repr
can include a pygmentize coloration for viewing.

"""


class ByteSize(int):
    """Store an human readable byte number. (extends int())
    >>> size = ByteSize("1 kb")
    >>> size()
    1024
    >>> print(size)
    1 KiB (1024 bytes)

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

        return( int.__new__(cls, result) )


    def __call__(self):
        return( int(self) )


    def __repr__(self):
        self_str = super(ByteSize, self).__str__()
        if self == 1:
            return("1 byte")

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
            result += " (%s bytes)" %self_str

        return(result)

