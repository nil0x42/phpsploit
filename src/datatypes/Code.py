try:
    import pygments
    import pygments.formatters
    import pygments.lexers
    import ui.output
    USE_PYGMENTS = True
except ImportError:
    USE_PYGMENTS = False


def Code(language):

    class ColoredCode(str):
        """Piece of source code. (extends str)
        Takes a string representing a portion of source code.

        When printed or when self.__str__() is called the code will be
        formated using pygments if possible. self._code_value() is used
        to retrieve the code to be formated, its default implementation
        is to use self.__call__().
        """

        if USE_PYGMENTS:
            lexer = pygments.lexers.get_lexer_by_name(language)
            if ui.output.colors() >= 256:
                formatter = pygments.formatters.Terminal256Formatter
            else:
                formatter = pygments.formatters.TerminalFormatter
            formatter = formatter(style='vim', bg='dark')

        def _raw_value(self):
            return super().__str__()

        def __call__(self):
            return self._raw_value()

        def _code_value(self):
            return self.__call__()

        def __str__(self):
            string = self._code_value()
            if not USE_PYGMENTS:
                return string
            return pygments.highlight(string,
                                      self.lexer,
                                      self.formatter).strip()

    return ColoredCode
