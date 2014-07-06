"""Print a file content to standard output

SYNOPSIS:
    cat <REMOTE FILE>

DESCRIPTION:
    This command prints the given file content on the standard
    output.

    NOTE: Unlike the GNU's 'cat' command, this plugin only takes
    one single file as argument, and have no support for multi
    file concatenation to standard output.

EXAMPLES:
    > cat ../includes/connect.inc.php
      - Display the connect.inc.php's content.
    > cat "C:\\Users\\granny\\Desktop\\bank account.TXT"
      - Don't be evil with grannies!
        NOTE: since gannies use spaces in file names, the path
        string must be enquoted to be considered as a single
        argument.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys
import base64

from api import plugin
from api import server
from api import environ

# from core import session

if len(plugin.argv) != 2:
    sys.exit(plugin.help)

relative_path = plugin.argv[1]
absolute_path = server.path.abspath(relative_path)

# if relative_path.endswith(environ['PATH_SEP']):
#     sys.exit(plugin.help)

payload = server.payload.Payload("payload.php")
payload['FILE'] = absolute_path

response = payload.send()

print(response)
