r"""Print a file content on standard output

SYNOPSIS:
    cat <REMOTE-FILE>

DESCRIPTION:
    Print REMOTE-FILE content on standard output.

LIMITATIONS:
    Unlike the standard GNU's 'cat' tool, multiple files cat
    is not supported.

EXAMPLES:
    > cat ../includes/connect.inc.php
      - Display the connect.inc.php's content.
    > cat "C:\Users\granny\Desktop\bank account.TXT"
      - Don't be evil with grannies!
      - As gannies use spaces in file names, the path
        must be quoted to be parsed as a single argument.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys
import base64

from core import encoding

from api import plugin
from api import server

if len(plugin.argv) != 2:
    sys.exit(plugin.help)

relative_path = plugin.argv[1]
absolute_path = server.path.abspath(relative_path)

payload = server.payload.Payload("payload.php")
payload['FILE'] = absolute_path

response = payload.send()

data = encoding.decode(base64.b64decode(response))
print(data)
