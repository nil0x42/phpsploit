"""Find open ports

SYNOPSIS:
    > scan <address> [-p <PORT>] [-t <TIMEOUT>]
      -p  Single or range port(s) to scan
          * single : -p port
          * range  : -p min-max
      -t  Timeout socket

EXAMPLES:
    > scan 192.168.1.10
      - find open port from 20 to 10000
    > scan 192.168.1.10 -p 50
      - find open port 50
    > scan 192.168.1.10 -p 50-100
      - find open port from 50 to 100
    > scan 192.168.1.10 -t 0.5
      - scan with 0.5 second timeout per socket

AUTHOR:
    Shiney <http://goo.gl/D6g4wl>
"""
import sys
import time

import os
from api import plugin
from api import server

import json
import plugin_args

if len(plugin.argv) < 2:
    sys.exit(plugin.help)

opt = plugin_args.parse(plugin.argv[1:])

# Send payload
payload = server.payload.Payload("scanner.php")
payload['IP'] = opt['address']
payload['PORT_MIN'] = opt['port'][0]
payload['PORT_MAX'] = opt['port'][1]
payload['TIMEOUT'] = opt['timeout']
print(opt['timeout'])
open_ports = payload.send()


# Load port -> service database
with open(os.path.join(plugin.path, "ports.json")) as database_ports:
    ports = json.load(database_ports)
# Print result
print(' ' * 3 + ' PORT ' + ' ' * 2 + ' PROBABLE SERVICE')
print('-' * 25)
for open_port in open_ports:
    print("%8s | %s" % (open_port, ports[str(open_port)] if str(open_port) in ports else ' '))

sys.exit(0)


