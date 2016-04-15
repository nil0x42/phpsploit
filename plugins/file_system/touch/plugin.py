"""Change file timestamps

SYNOPSIS:
    touch [OPTION]... <REMOTE_FILE>

OPTIONS:
    -t <STAMP>
        use YYYY[-mm[-dd[ HH[:MM[:SS]]]]] instead of current time
        NOTE: If partially defined (e.g: yyyy/mm only), other
              values will be randomly chosen.

DESCRIPTION:
    Update the access and modification times of <REMOTE FILE>
    to the current time.

    If <REMOTE FILE> does not exist, it is created empty

EXAMPLES:
    > touch file.txt
      - Set file atime/mtime to current time
    > touch -t '2012/12/21 23:59:59' file.txt
      - Set file atime/mtime to Dec 21 23:59:59 2012
    > touch -t '2015' file.txt
      - Set file atime/mtime to a random date in 2015

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys

import utils

from api import plugin
from api import server

if len(plugin.argv) == 2:
    timestamp = None
    relative_path = plugin.argv[1]
elif len(plugin.argv) == 4 and plugin.argv[1] == '-t':
    timestamp = utils.time.get_smart_date(plugin.argv[2])
    relative_path = plugin.argv[3]
else:
    sys.exit(plugin.help)

absolute_path = server.path.abspath(relative_path)

payload = server.payload.Payload("payload.php")
payload['FILE'] = absolute_path
payload['TIME'] = timestamp

response = payload.send()
assert response == 'OK'
