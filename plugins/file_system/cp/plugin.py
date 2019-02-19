r"""Copy a file between two remote paths

SYNOPSIS:
    cp [-f] <REMOTE-FILE> <REMOTE-DESTINATION>

OPTIONS:
    -f
        overwrite REMOTE-DESTINATION without user confirmation.

DESCRIPTION:
    Copy a remote file to another remote destination.
    - REMOTE-FILE must be readable.
    - REMOTE-DESTINATION must be a writable file or directory.
    - If REMOTE-DESTINATION is a directory, REMOTE-FILE will
    be copied into it, preserving original file name.
    - Unless '-f' option has been provided, user confirmation is
    needed to overwrite REMOTE-DESTINATION (if it already exists).

LIMITATIONS:
    Unlike the standard GNU's 'cp' tool, recursive directory
    and multiple file copy are not available.

EXAMPLES:
    > cp -f exploit.php ../images/archive/IMG0043.PHP
      - Copy an exploit to a stealth location, force copy.
    > cp \Bach\LOG\ex191213.zip C:\intepub\wwwroot\x.zip
      - Copy this interesting file to a web accessible path.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys

from api import plugin
from api import server

argc = len(plugin.argv)

if argc not in [3, 4]:
    sys.exit(plugin.help)

payload = server.payload.Payload("payload.php")
payload['FORCE'] = 0

src_arg, dst_arg, arglen = [1, 2, argc]
if plugin.argv[1] == '-f':
    payload['FORCE'] = 1
    src_arg, dst_arg, arglen = [2, 3, (argc - 1)]

if arglen != 3:
    sys.exit(plugin.help)

payload['SRC'] = server.path.abspath(plugin.argv[src_arg])
payload['DST'] = server.path.abspath(plugin.argv[dst_arg])

src, dst = payload.send()

print("Copy complete: '%s' -> '%s'" % (src, dst))
