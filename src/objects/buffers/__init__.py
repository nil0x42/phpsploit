"""Special buffers for settings type wrapping.

The `objetcs.buffers` submodule includes wrappers for
session settings buffers management.

Actually, 2 buffers are available:
------------------------------------

MultilineBuffer()
    This type makes the setting bindable to a common file
    of a multiline stored buffer.
    Anyway, the value of the variable is multiline.

RandlineBuffer()
    Parent class: MultiLineBuffer()
    A setting using this buffer as wrapper binds to a
    file or a multiline stored buffer, except that acessing
    its value (by __call__() method) returns a randomly
    picked line from the buffer, instead of returning the
    whole buffer like does the MutiLineBuffer() buffer.


NOTE: For more informations about basic behavior of settings
buffers, take a look at the MultiLineBuffer class docstrings.

"""

from .MultiLineBuffer import MultiLineBuffer
from .RandLineBuffer  import RandLineBuffer
