"""Run a python console at runtime from Phpsploit
"""
__all__ = ["Console"]

import traceback
# alias exit() to prevent I/O fd closure bug on Console() interpreter
# pylint: disable=redefined-builtin,unused-import
from sys import exit

from ui.color import colorize
from decorators.isolate_readline_context import isolate_readline_context


class Console:
    """Create a python console to be run at phpsploit runtime

    In order of preference, it tries to run 'bpython' then 'IPython'.
    If none of these interpreters can be found, it defaults to
    default_console() method.

    >>> c = Console("Python console")

    >>> c()
    Python console
    > print(len([1,2,3]))
    3
    """
    def __init__(self, banner="Python console"):
        self.banner = banner

    @isolate_readline_context
    def __call__(self):
        """Execute the best available python console

        This method trie to run the best available
        python console (bpython and ipython).
        Otherwise, it fallbacks to default_console()
        method.

        Finally, the chosen console method is executed.

        NOTE: This method is wrapped with the
              `@isloate_io_context` decorator.
        """
        try:
            import bpython
            del bpython
            console = self.bpython_console
        except ImportError:
            try:
                import IPython
                del IPython
                console = self.ipython_console
            except ImportError:
                console = self.default_console
        return console()

    def default_console(self):
        """Simple python console interpreter

        Used as fallback when neither of other consoles are available
        It basically consists in an exec(input("> ")) loop
        """
        print(colorize("%BoldWhite", self.banner))
        while True:
            try:
                # pylint: disable=exec-used
                exec(input("> "))
            except EOFError:
                print()
                return 0
            except SystemExit as e:
                if e.code is not None:
                    print(e.code)
                return int(bool(e.code))
            except BaseException as e:
                e = traceback.format_exception(type(e), e, e.__traceback__)
                e.pop(1)
                print(colorize("%Red", "".join(e)))

    def bpython_console(self):
        """bpython console interpreter

        https://bpython-interpreter.org/
        """
        # pylint: disable=import-error
        import bpython
        bpython.embed(banner=self.banner)
        return 0

    def ipython_console(self):
        """IPython console interpreter

        https://ipython.org/
        """
        # pylint: disable=import-error
        import IPython
        print(colorize("%BoldWhite", self.banner))
        IPython.embed()
        return 0
