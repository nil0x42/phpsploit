"""Backward compatibility libraries

This module provides a collection of phpsploit
components which aim to be used as fallbacks
with older versions of the framework.

Currently, the backwards compatibility module
is split into two submodules, for each old
core version of the framework:

    * v1 : Refers to phpsploit legacy, a very
           old and stupid implementation, wich
           has been used circa 2011.
           The phpsploit session fromat was
           a text-mode pickle dump, without
           PSCOREVER tag.

    * v2 : Refers to phpsploit version 2,
           until version `2.1.4`.
           Session files from this core version
           can be recognized by the use of
           text-based pickle dump with use
           of a PSCOREVER tag, set to 2.

"""

from . import v1
from . import v2
