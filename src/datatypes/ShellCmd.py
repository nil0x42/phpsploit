import os
from shnake import parse
from ui.color import colorize

from .Code import Code

class ShellCmd(Code("sh")):
    """ShellCmd is an executable program or shell command. (extends str)

    Takes an executable program path or shell command.

    >>> text_editor = ShellCmd('vim')
    >>> text_editor()
    "vim"

    """
    def __new__(cls, executable):
        try:
            cmds = parse(executable)
        except SyntaxError:
            raise ValueError("«%s» is not a valid shell command" % executable)

        # Value is OK, now we maintain original.
        return str.__new__(cls, executable)
