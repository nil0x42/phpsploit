"""Phpsploit operations on target server.

This module includes a collection of submodules
designed for phpsploit server-side operations.

CONTENTS:

* path (type: submodule)
    Common operation on target server pathnames.

* payload (type: submodule)
    The phpsploit payload request manager.
"""


from . import path
from . import payload
