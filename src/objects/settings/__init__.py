"""Special metatypes for settings type wrapping.

This `objects` submodule contains all objects used by the
phpsploit's session settings.

`metatypes` are wrappers for those settings.

Actually, 2 metatypes are available:
------------------------------------

MultilineBuffer()
    This type makes the setting bindable to a common file
    of a multiline stored buffer.
    Anyway, the value of the variable is multiline.

RandlineBuffer()
    Parent class: MultiLineBuffer()
    A setting using this metatype as wrapper binds to a
    file or a multiline stored buffer, except that acessing
    its value (by __call__() method) returns a randomly
    picked line from the buffer, instead of returning the
    whole buffer like does the MutiLineBuffer() metatype.


NOTE: For more informations about basic behavior of settings
metatypes, take a look at the MultiLineBuffer class docstrings.

"""

from .MultiLineBuffer import MultiLineBuffer
from .RandLineBuffer  import RandLineBuffer
