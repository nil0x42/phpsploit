"""

Contents Preview / Examples:
============================

------------ ui.input ---------------------

>>> import ui.input

>>> if ui.input.Expect(False)('Leave the shell ?'):
...     exit('shell left')

>>> ui.input.Expect(timeout=60)('Press enter or wait 1 minut to pursue')



------------ ui.output --------------------

>>> import ui.output

>>> print('current output supports %s colors' %ui.output.colors() )

>>> print('terminal size is %s' %ui.output.size() )

>>> if not ui.output.isatty():
...     INTERACTIVE = False

>>> import sys
>>> sys.stdout = ui.output.Wrapper(backlog=True)



------------ ui.color ---------------------

>>> import ui.color

>>> colorString = ui.color.colorize('Hello ', '%DimRed', 'World !')

>>> blankString = ui.color.decolorize(colorString)



------------ ui.interface -----------------

>>> import ui.interface

>>> interface = ui.interface.Cmd()
>>> interface.cmdloop()


------------ ui.console -------------------

>>> import ui.console

>>> console = ui.console.Console()
>>> console()

------------ ui.isatty --------------------

>>> import ui
>>> ui.isatty()
True  # or False maybe...



"""

from . import input
from . import output


# returns True it both stdin and stdout are tty
isatty = lambda: input.isatty() and output.isatty()
