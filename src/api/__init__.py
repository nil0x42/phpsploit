"""Phpsploit plugin developer API

This package includes the python-side plugin
development API.

CONTENTS:

* plugin (type: api.plugin.Plugin())
    Contains current plugin attributes.

* environ (type: dict)
    Get enviromnent variables of current phpsploit session.

* server (type: module)
    This module includes target server related operations.
    It actually contains the following submodules:
        - path: For common operations on server pathnames.
        - payload: The phpsploit payload requests manager.
"""


# Import api.server package
from . import server

# Define api.plugin (current plugin attributes)
from .plugin import plugin

# Define api.environ dictionary (environment variables)
from core import session
environ = session.Env
del session
