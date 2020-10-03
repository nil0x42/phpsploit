"""TCP Banner Grabber

SYNOPSIS:
    bannergrab <address> [-p <PORT>] [-t <TIMEOUT>]
      -p  single or range of port(s) to connect to
          * single : -p port
          * range  : -p min-max
      -t  socket timeout

DESCRIPTION:
    Connect to a single port or range of ports and grab the
    application banner

EXAMPLES:
    > bannergrab 192.168.1.10
      - find TCP banners from port 20 to 10000
    > bannergrab 192.168.1.10 -p 50
      - find TCP banners on port 50
    > bannergrab 192.168.1.10 -p 50-100
      - find TCP banners from ports 50 to 100
    > bannergrab 192.168.1.10 -t 0.5
      - connect with 0.5 second timeout per socket

AUTHOR:
    Jose <https://twitter.com/jnazario>
"""

import sys

from api import plugin
from api import server

from ui.color import colorize
import plugin_args

if len(plugin.argv) < 2:
    sys.exit(plugin.help)

opt = plugin_args.parse(plugin.argv[1:])

# Send payload
payload = server.payload.Payload("payload.php")
payload['IP'] = opt['address']
payload['PORT_MIN'] = opt['port'][0]
payload['PORT_MAX'] = opt['port'][1]
payload['TIMEOUT'] = opt['timeout']

result = payload.send()

# unshuffle port list
result.sort(key=lambda x: x[0])


fmt = "%4s   %7s   %s"
print(fmt % ("PORT", "STATE", "INFORMATION"))
print(fmt % ("----", "-----", "-----------"))
for port, state, banner in results:
    if state == "OPEN":
        state = colorize("%Green", "open")
    else:
        state = colorize("%Red", "closed")
    print(fmt % (port, state, banner))
