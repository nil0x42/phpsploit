from re import match as regex_match
import output

class PhpCode(str):
    """Line of PHP Code. (extends str)

    Takes a string representing a portion of PHP code.

    >>> code = PhpCode('<? phpinfo() ?>')
    >>> code()
    'phpinfo();'
    >>> print(code)
    '<?php phpinfo(); ?>'

    """
    _pattern = ("^\s*(?:<\?(?:[pP][hH][pP])?\s+)?\s*("
                "[^\<\s].{4,}?)\s*;?\s*(?:\?\>)?\s*$")

    def __new__(cls, string):
        # regex validates and parses the string
        try:
            php = re.match(cls._pattern, string).group(1)
        except:
            raise ValueError('«%s» is not PHP code' %string)

        return str.__new__(cls, php)


    def __raw_value(self):
        return super(PhpCode, self).__str__()


    def __call__(self):
        return self.__raw_value()


    def __str__(self):
        string = "<?php %s; ?>" %self.__call__()
        # colored representation depends on pygments lib.
        try:
            import pygments
            import pygments.formatters
            from pygments.lexers import PhpLexer as lexer
            assert output.colors()
        except:
            return string

        # 265 colors will be used if current output supports them
        if output.colors() >= 256:
            formatter = pygments.formatters.Terminal256Formatter
        else:
            formatter = pygments.formatters.TerminalFormatter

        return pygments.highlight(string, lexer(), formatter(style='tango'))
