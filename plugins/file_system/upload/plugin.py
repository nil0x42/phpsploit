"""Upload a file

SYNOPSIS:
    upload [-f] <LOCAL-FILE> [<REMOTE-DESTINATION>]

OPTIONS:
    -f      Overwrite destination without confirmation if it
            already exists.

DESCRIPTION:
    Upload a local file to the remote server.
    - LOCAL-FILE must be readable.
    - REMOTE-DESTINATION must be a writable file or directory.
    - If REMOTE-DESTINATION is a directory, LOCAL-FILE will be
    uploaded into it, preserving original file name.
    - If REMOTE-DESTINATION is not provided, LOCAL-FILE is uploaded
    to remote current working directory (which can be known with
    the `pwd` command).
    - Unless '-f' option has been provided, user confirmation is
    needed to overwrite REMOTE-DESTINATION (if it already exists).
    NOTE: If the user confirms REMOTE-DESTINATION overwrite,
    another HTTP request will be sent to upload the file.

LIMITATIONS:
    Recursive directory and multiple file uploads are not available.

EXAMPLES:
    > upload /data/backdoors/r75.php /var/www/images/
      - Upload your local r57.php file to the remote images dir
    > upload -f /tmp/logo-gimped.png /srv/www/img/logo.png
      - Overwrite the remote logo with your own without confirm
    > upload C:\\Users\\blackhat\\index.php
      - Upload your index.php to the remote server's current
        working directory. If your location is a web root path
        which already contains an index.php, then you must
        answer to the confirmation request.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys
import os
import base64

import utils
import ui.input

from api import plugin
from api import server

# parse arguments
if not 2 <= len(plugin.argv) <= 4:
    sys.exit(plugin.help)

if plugin.argv[1] == "-f":
    force = True
    arg1 = 2
    arg2 = 3
    arglen = len(plugin.argv) - 1
else:
    force = False
    arg1 = 1
    arg2 = 2
    arglen = len(plugin.argv)

if arglen == 3:
    relpath = plugin.argv[arg2]
else:
    relpath = server.path.getcwd()
abspath = server.path.abspath(relpath)

local_relpath = plugin.argv[arg1]
local_abspath = utils.path.truepath(local_relpath)
local_basename = os.path.basename(local_abspath)

# check for errors
if not os.path.exists(local_abspath):
    sys.exit("Can't upload %s: No such file or directory" % local_abspath)

if not os.path.isfile(local_abspath):
    sys.exit("Can't upload %s: Not a file" % local_abspath)

try:
    data = open(local_abspath, 'rb').read()
except OSError as e:
    sys.exit("Can't upload %s: %s" % (e.filename, e.strerror))

# send the payload (twice if needed)
payload = server.payload.Payload("payload.php")
payload['TARGET'] = abspath
payload['NAME'] = local_basename
payload['DATA'] = base64.b64encode(data)
payload['FORCE'] = force

for iteration in [1, 2]:
    if iteration == 2:
        payload['FORCE'] = True

    status, uploaded_file = payload.send()

    if status == 'KO':
        question = "Remote destination %s already exists, overwrite it ?"
        if ui.input.Expect(False)(question % uploaded_file):
            sys.exit("File transfer aborted")
        else:
            continue

    print("[*] Upload complete: %s -> %s" % (local_abspath, uploaded_file))
    sys.exit(0)
