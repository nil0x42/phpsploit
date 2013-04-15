"""Useful data types collection

This package includes some useful data types, which supports
dynamic value and enhanced representations.
It has been developped in order to properly handle the PhpSploit
framework's session settings and environment variables.

PhpSploit dedicated datatypes obey the following conventions:
  * The __str__ method returns an human readable representation, with
    ANSI colors (handled by the termcolor library).
  * The __call__ method gives a concretely usable value, which in some
    cases is dynamic (Interval type returns a random float from range).
    Non dynamic values also must provide a call, with in this case
    gives the raw value. (the tuple from interval for example)
  * Each data type extends a built-in data type, related to it's master
    value. (interval's master value is a tuple of floats)

Examples:
>>> import datatypes
>>> REQ_INTERVAL = datatypes.Interval('1.5 < 5')
>>> REQ_INTERVAL
(1.0, 5.0)
print(REQ_INTERVAL)
1.5 < 5 (random interval)
>>> REQ_INTERVAL()
4.2

"""

from .ByteSize    import ByteSize
from .WritableDir import WritableDir
from .Executable  import Executable
from .Interval    import Interval
#from .PhpCode     import PhpCode
#from .Proxy       import Proxy
from .Url         import Url
