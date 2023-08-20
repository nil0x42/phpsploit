r"""Move a file between two remote paths

SYNOPSIS:
    mv <REMOTE-FILE> <REMOTE-DESTINATION>

DESCRIPTION:
    Move a remote file to another remote destination.
    - REMOTE-FILE must be readable.
    - REMOTE-DESTINATION must be a writable directory.
    - If REMOTE-DESTINATION is a directory, REMOTE-FILE will

LIMITATIONS:
    rename() is working on Linux/UNIX but not working on Windows on a directory containing a file formerly opened within the same script.
    The problem persists even after properly closing the file and flushing the buffer.


EXAMPLES:
    > mv \Bach\LOG\ex191213.zip C:\intepub\wwwroot\x.zip
      - Move this interesting file to a web accessible path.

AUTHOR:
    Nader-abdi <https://github.com/Nader-abdi>
"""

import sys

from api import plugin
from api import server

argc = len(plugin.argv)

if argc not in [3, 4]:
    sys.exit(plugin.help)

payload = server.payload.Payload("payload.php")

src_arg, dst_arg, arglen = [1, 2, argc]


if arglen != 3:
    sys.exit(plugin.help)

payload['SRC'] = server.path.abspath(plugin.argv[src_arg])
payload['DST'] = server.path.abspath(plugin.argv[dst_arg])

src, dst = payload.send()

print("Move complete: '%s' -> '%s'" % (src, dst))
