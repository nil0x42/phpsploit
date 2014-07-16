"""Run a python console at phpsploit runtime

This module has workaround for bpython an IPython.
If none of those is available, the console fallbacks
to a basic and dirty python interpreter.

"""

import traceback
from sys import exit  # alias exit() to prevent I/O bug due to fd closure.

from ui.color import colorize
from decorators import isolate_io_context


class Console:

    def __init__(self, banner="Python console"):
        self.banner = banner

    @isolate_io_context
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
        print(colorize("%BoldWhite", self.banner))
        while True:
            try:
                exec(input("> "))
            except EOFError:
                return 0
            except SystemExit as err:
                if err.code is not None:
                    print(err.code)
                return int(bool(err.code))
            except BaseException as e:
                e = traceback.format_exception(type(e), e, e.__traceback__)
                e.pop(1)
                print(colorize("%Red", "".join(e)))

    def bpython_console(self):
        import bpython
        bpython.embed(banner=self.banner)
        return 0

    def ipython_console(self):
        print(colorize("%BoldWhite", self.banner))
        import IPython
        IPython.embed()
        return 0
