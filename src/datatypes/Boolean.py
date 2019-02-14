from ui.color import colorize


class Boolean(int):
    """High level boolean representation. (extends int)

    This datatype could be instanciated by passing a string
    "True" of "False", both case insensitive.
    It also can pass an int, 0 meaning false, and anything else
    true.

    >>> Boolean("fAlSe")
    False
    >>> Boolean(1)
    True
    >>> Boolean(False)
    False
    """

    def __new__(cls, value):
        try:
            value = int(value)
        except ValueError:
            value = str(value).capitalize()
            if value == "False":
                value = False
            elif value == "True":
                value = True
            else:
                raise ValueError("boolean must be True/False")
        return int.__new__(cls, value)

    def _raw_value(self):
        return int(self)

    def __call__(self):
        return self._raw_value()

    def __str__(self):
        return colorize("%BoldCyan", "True" if self else "False")
