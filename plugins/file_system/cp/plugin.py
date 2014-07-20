"""Copy a file between two remote paths

SYNOPSIS:
    cp [-f] <REMOTE-FILE> <REMOTE-DESTINATION>

OPTIONS:
    -f      Overwrite destination without confirmation if it
            already exists.

DESCRIPTION:
    A basic GNU's 'cp' tool simulation, which acts copying the
    file given as first argument, to the location defined by
    second argument.
    The file to copy must be at least readable, and the
    destination can be a file path, or a directory path.
    - In the case the destination is a directory, the file will
    be copied into it keeping it's original file name.
    - Unless the '-f' option has been set, the copy process
    aborts if the detination file already exists, and asks for
    an confirmation to overwrite the file.

    NOTE: Unlike the standard GNU's 'cp' tool, this plugin can
    not copy more than one file at the time.

EXAMPLES:
    > cp -f exploit.php ../images/archive/IMG0043.PHP
      - Copy an exploit to a stealth location, force copy.
    > cp \\Bach\\LOG\\ex191213.zip C:\\intepub\\wwwroot\\x.zip
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
