"""Create directory

SYNOPSIS:
    mkdir [-p] <REMOTE-DIRECTORY>

OPTIONS:
    -p
        no error if existing, make parent directories as needed.

DESCRIPTION:
    The 'mkdir' plugin creates REMOTE-DIRECTORY. It reports
    an error if it already exists.
    - Unless '-p' option is provided, parent directory must exist.

LIMITATIONS:
    Unlike GNU's mkdir core util, this plugin does not support
    multiple path arguments.

EXAMPLES:
    > mkdir includes
      - Create the 'includes' directory from current location
    > mkdir /srv/www/data/img/thumb/
      - Create the 'thumb' directory if it's parent exists
    > mkdir /srv/www/data/img/thumb/
      - Create the 'thumb' directory even if parent don't exist
    > mkdir -p /var/www/a/b/c/d/e/f/g/h/
      - Create 'h/' directory, and parent directories as needed.

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
