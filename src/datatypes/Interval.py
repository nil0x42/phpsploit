from re import split as regex_split
from random import uniform as random
from ui.color import colorize


class Interval(tuple):
    """Random float from interval numbers. (extends tuple)

    Static values can be defined by giving a single number, as an
    int, float or str. The returned float will then never change.

    Dynamic values can be defined by giving a couple of numbers, in
    tuple or str format. If str, is must contain two numbers
    separated by any one other char(s) (e.g. "between 1.2 and 12").

    >>> val = Interval("1,5 < 5")
    >>> val
    (1.5, 5.0)
    >>> val()
    4.2
    >>> print(val)
    1.5 <= x <= 5 (random interval)

    """
    def __new__(cls, value):
        rawval = str(value)
        if type(value) in (int, float, str):
            value = str(value).replace(',','.')
            value = regex_split('[^0-9.]', value)

        value = [str(e) for e in value if e]
        if len(value) == 1:
            value = [value[0], value[0]]

        try:
            assert len(value) == 2
            value = tuple(sorted([float(e) for e in value]))
        except:
            raise ValueError('«%s» must be an int/float interval'
                             ' representation' %rawval)

        return tuple.__new__(cls, value)


    def _raw_value(self):
        return tuple(self)


    def __call__(self):
        return random(self[0], self[1])


    def __str__(self):
        low, big = [str(x).rstrip('0').rstrip('.') for x in self]
        main = colorize('%Bold', '%s', '%Basic')

        if low is big:
            text = main %low
            comment = '(fixed interval)'
        else:
            text = ' <= '.join((low, main %'x', big))
            comment = '(random interval)'

        return colorize('%Pink', text, " ", '%DimWhite', comment)
