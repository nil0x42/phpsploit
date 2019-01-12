"""Remove empty directory

SYNOPSIS:
    rmdir <REMOTE-DIRECTORY>

DESCRIPTION:
    Remove REMOTE-DIRECTORY if it is empty.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys

from api import plugin
from api import server

if len(plugin.argv) != 2:
    sys.exit(plugin.help)

rel_path = plugin.argv[1]
abs_path = server.path.abspath(rel_path)

payload = server.payload.Payload("payload.php")
payload["DIR"] = abs_path

payload.send()
