"""Create directory

SYNOPSIS:
    mkdir [-p] <REMOTE DIRECTORY>

OPTIONS:
    -p      No error if existing, make parent directories as
            needed.

DESCRIPTION:
    The 'mkdir' plugin creates the REMOTE DIRECTORY. It reports
    an error if the path already exists, unless the '-p' option
    is given and the path is a directory.

    NOTE: Unlike the GNU's mkdir core util, this plugin only
    supports single directory creation, no multiple path
    arguments are supported, at least for the moment.

EXAMPLES:
    > mkdir includes
      - Create the 'includes' directory from current location
    > mkdir /srv/www/data/img/thumb/
      - Create the 'thumb' directory if it's parent exists
    > mkdir /srv/www/data/img/thumb/
      - Create the 'thumb' directory even if parent don't exist

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys

from api import plugin
from api import server
from api import environ

if len(plugin.argv) == 2 and plugin.argv[1] != '-p':
    relpath = plugin.argv[1]
elif len(plugin.argv) == 3 and plugin.argv[1] == '-p':
    relpath = plugin.argv[2]
else:
    sys.exit(plugin.help)

abspath = server.path.abspath(relpath)

if plugin.argv[1] == '-p':
    payload = server.payload.Payload("parent.php")
    drive, path = server.path.splitdrive(abspath)
    payload['DRIVE'] = drive
    payload['PATH_ELEMS'] = [x for x in path.split(environ['PATH_SEP']) if x]
else:
    payload = server.payload.Payload("payload.php")
    payload['DIR'] = abspath

payload.send()
