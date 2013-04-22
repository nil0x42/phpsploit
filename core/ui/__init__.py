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



------------ ui.shell ---------------------

>>> import ui.shell

>>> interface = ui.shell.Main()
>>> interface.cmdloop()

"""
