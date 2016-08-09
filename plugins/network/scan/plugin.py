"""Find open ports

SYNOPSIS:
    > scan <ip> <port min> <port max>


EXAMPLES:
    > scan 192.168.1.10
      - find open port from 20 to 10000
    > scan 192.168.1.10 50
      - find open port from 50 to 10000
    > scan 192.168.1.10 50 100
      - find open port from 50 to 100

AUTHOR:
    Shiney <http://goo.gl/D6g4wl>
"""
import sys
import time

import os
from api import plugin
from api import server
from api import environ
import json

if len(plugin.argv) < 2:
    sys.exit(plugin.help)


# Load port -> service database
with open(os.path.dirname(__file__) + '/ports.json') as database_ports:
    ports = json.load(database_ports)

# Send payload
payload = server.payload.Payload("scanner.php")
payload['IP'] = plugin.argv[1]
payload['PORT_MIN'] = plugin.argv[2] if len(plugin.argv) > 2 else 20
payload['PORT_MAX'] = plugin.argv[3] if len(plugin.argv) > 3 else 10000
open_ports = payload.send()

# Print result
print(' ' * 3 + ' PORT ' + ' ' * 2 + ' PROBABLE SERVICE')
print('-' * 25)
for open_port in open_ports:
    print("%8i | %s" % (open_port, ports[str(open_port)] if str(open_port) in ports else ' '))

sys.exit(0)


