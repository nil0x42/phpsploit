"""Client for ldap

SYNOPSIS:
    ldap connect <HOST> [<LOGIN> <PASSWORD>]
    ldap list <DN>
    ldap search <DN> <FILTER>
    ldap set [<KEY> <VAL>]

DESCRIPTION:
    > ldap connect <HOST> [<LOGIN> <PASSWORD>]
        Connect to service
    > ldap list <DN>
        List node
    > ldap search <DN> <FILTER>
        Find node based on filter
    > ldap set
        List env var
    > ldap set <KEY> <VAL>
        Set env var
EXAMPLES:
    > ldap connect 10.0.0.100
      - Connect anonymously to 10.0.0.100
    > ldap connect 10.0.0.100 "cn=admin,dc=example,dc=org" admin
      - Connect to 10.0.0.100 as "admin" with password "admin"
    > ldap list "dc=example,dc=org"
    > ldap search "dc=example,dc=org" "userpassword=*"
    > ldap set VERSION 3
      - Set LDAP protocol V3

AUTHOR:
    Shiney <http://goo.gl/D6g4wl>
"""

import sys

from api import plugin
from api import server
from api import environ
import objects
from ui.color import colorize


def print_node(node):
    if 'dn' in node:
        print(colorize('%BlueBold', node['dn']))
    else:
        print(colorize('%BlueBold', '----------------------'))

    for key, val in node.items():
        if isinstance(val, dict):
            del val['count']
            line = "   %s :  %s" % (colorize('%Bold', "%20s" % key), ' | '.join(val.values()))
            print(line)
    print()


if len(plugin.argv) < 2:
    sys.exit(plugin.help)

# Set env var
if plugin.argv[1].lower() == "set":
    if len(plugin.argv) < 3:
        print(environ['LDAP'])
        sys.exit(0)
    if len(plugin.argv) < 4:
        print('Missing parameter\n> ldap set VAR value')
        sys.exit(0)
    if plugin.argv[2].upper() in environ['LDAP']:
        environ['LDAP'][plugin.argv[2].upper()] = plugin.argv[3]
    else:
        sys.exit('This setting doesn\'t exist')
    sys.exit(0)

# Connecting to service
if plugin.argv[1].lower() == "connect":
    if 3 < len(plugin.argv) < 5:
        sys.exit("Missing parameter")
    environ['LDAP'] = objects.VarContainer(title="LDAP settings")

    environ['LDAP']['HOST']    = plugin.argv[2]
    environ['LDAP']['LOGIN']   = plugin.argv[3] if len(plugin.argv) > 3 else " "
    environ['LDAP']['PASS']    = plugin.argv[4] if len(plugin.argv) > 4 else " "
    environ['LDAP']['VERSION'] = 3
    sys.exit(0)
# check and load MYSQL_CRED environment variable
if "LDAP" not in environ:
    sys.exit("Not connected to any server, use `ldap connect` before")

# List node
if plugin.argv[1].lower() == "list":
    if len(plugin.argv) < 3:
        sys.exit("Missing parameter")
    payload = server.payload.Payload("list.php")
    payload.update(environ['LDAP'])
    payload['BASE_DN'] = plugin.argv[2]
    response = payload.send()

    if response['count'] == 0:
        print('No result')
        sys.exit(0)

    for k, row in response.items():
        if k == 'count':
            continue
        print_node(row)
    pass

# Search node
if plugin.argv[1].lower() == "search":
    if len(plugin.argv) < 4:
        sys.exit("Missing parameter")
    payload = server.payload.Payload("search.php")
    payload.update(environ['LDAP'])
    payload['BASE_DN'] = plugin.argv[2]
    payload['SEARCH'] = plugin.argv[3]
    response = payload.send()

    if response['count'] == 0:
        print('No result')
        sys.exit(0)

    for k, row in response.items():
        if k == 'count':
            continue
        print_node(row)
    pass

sys.exit(0)
