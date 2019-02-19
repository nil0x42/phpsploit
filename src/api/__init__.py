"""Phpsploit plugin developer API

This package includes the python-side plugin
development API.

CONTENTS:

* plugin (type: api.plugin.Plugin())
    Access running plugin attributes

* environ (type: dict)
    Access phpsploit session's Environment Variables

* server (type: package)
    Provides target server related operations.
    Modules:
      - path: Remote server pathname operations.
      - payload: Run a PHP payload on remote server.
"""
__all__ = ["plugin", "environ", "server"]

from core import session

# Define api.plugin (current plugin attributes)
from .plugin import plugin

# Import api.server package
from . import server

# Define api.environ dictionary (environment variables)
environ = session.Env
del session
