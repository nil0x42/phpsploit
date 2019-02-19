r"""Change directory

SYNOPSIS:
    cd [<DIRECTORY>]

DESCRIPTION:
    Change current working directory of phpsploit target.

    - This plugin checks if the given path is remotely
    reachable, then changes $PWD environment variable if
    no errors were found.
    - If run without argument, $HOME env var is used as
    new current working directory.

EXAMPLES:
    > cd ..
      - Go to the directory below
    > cd "C:\Program Files\"
      - Go to "Program Files" directory
    > cd ~
      - Move the the user's HOME directory

ENVIRONMENT:
    * PWD
        The current remote working directory

WARNING:
    - Manual edition of the $PWD environment variable without using
    this plugin is usually a bad idea, because we take the risk
    to set it to an invalid location, without the checks done by
    this plugin.
    - Therefore, in a few use cases, manual edition of the $PWD
    variable is the only option.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys

from api import plugin
from api import server
from api import environ

if len(plugin.argv) > 2:
    sys.exit(plugin.help)

if len(plugin.argv) == 2:
    relative_path = plugin.argv[1]
else:
    relative_path = environ['HOME']

absolute_path = server.path.abspath(relative_path)

payload = server.payload.Payload("payload.php")
payload['DIR'] = absolute_path

response = payload.send()

if response != "ok":
    sys.exit("Unexpected response: %r" % response)

# change $PWD phpsploit environment variable
environ['PWD'] = absolute_path
