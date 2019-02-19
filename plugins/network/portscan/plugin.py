"""TCP port scanner

SYNOPSIS:
    portscan <HOST> [-p <PORT>] [-t <TIMEOUT>]

OPTIONS:
    -p <PORT>
        single or range of port(s) to scan
        (defaults to 20-10000)
    -t <TIMEOUT>
        socket timeout (in seconds)
        (defaults to 0.2)

DESCRIPTION:
    Scan a single port or range of ports on HOST

EXAMPLES:
    > portscan 192.168.1.10
      - scan default ports
    > portscan 192.168.1.10 -p 50
      - find if port 50 is open
    > portscan 192.168.1.10 -p 50-100
      - find if ports 50 to 100 are open
    > portscan 192.168.1.10 -t 0.5
      - scan with 0.5 second timeout per socket

AUTHOR:
    Shiney <http://goo.gl/D6g4wl>
"""

import sys
import os
import json

from api import plugin
from api import server

from ui.color import colorize
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

result = payload.send()

# unshuffle port list
result.sort(key=lambda x: x[0])

# Load port -> service database
with open(os.path.join(plugin.path, "ports.json")) as database_ports:
    known_services = json.load(database_ports)

# don't display most common error if frequent (nmap flavour)
main_err = [None, None]
errors = [tuple(x[1:]) for x in result if len(x) == 3]
if len(errors) > max(20, len(result) / 2):
    main_err = max(set(errors), key=errors.count)
    main_err_count = errors.count(main_err)
    if main_err_count == len(result):
        print("All %d scanned ports failed with error %d: %s\n"
              % (main_err_count, main_err[0], main_err[1]))
        sys.exit(0)
    print("Not shown: %d (%s)\n" % (main_err_count, main_err[1]))

# display each port with information
print("PORT   INFORMATION")
print("----   -----------")
for elem in result:
    port_num = str(elem[0])
    info = ""
    if len(elem) == 1:
        info = colorize("%Green", "open")
        if port_num in known_services.keys():
            info += " (%s)" % known_services[port_num]
    elif len(elem) == 3 and elem[1] != main_err[0]:
        info = colorize("%Red", elem[2])
    if info:
        print("{:<5}  {}".format(port_num, info))
