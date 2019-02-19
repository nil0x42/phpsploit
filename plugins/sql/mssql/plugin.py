r"""A client for Microsoft SQL Server

SYNOPSIS:
    mssql connect <USERNAME>@<HOSTNAME> [-p <PASSWORD>]
    mssql show [databases|tables]
    mssql use <DATABASE>
    mssql "<SQL COMMAND>"

DESCRIPTION:
    This plugin handles "Microsoft SQL Server" interactions
    through a mysql-like client approach.
    - The 'connect' argument establishes a connection with
    given credentials, which are then stored on `MSSQL_CRED`
    environment variable in order to be persistent between
    plugin calls in current session.
    - The 'use' argument can be used to choose a default
    database (stored in MSSQL_BASE environment variable).
    - Any other case assumes that the arguments are an SQL
    command, and result is returned.
    - A command that ends with '\G' will use tabular
    display mode.

WARNING:
    Considering the PhpSploit's input parser, commands which
    contain quotes, semicolons, and other chars that could be
    interpreted by the framework SHALL be enquoted to be
    interpreted as a single argument. For example:
      > run echo 'foo bar' > /tmp/foobar; cat /etc/passwd
    In this case, quotes and semicolons will be interpreted by
    the framework, so the correct syntax is:
      > run "echo 'foo bar' > /tmp/foobar; cat /etc/passwd"

EXAMPLES:
    > mssql connect SA@10.0.0.100 -p god123
      - Connect to 10.0.0.100 as "SA" with password "god123"
    > mssql show databases
      - Print the databases list (mysql client like)
    > mssql use master
      - Use the "master" database as default one
    > mssql SELECT * FROM sysusers
      - Print the whole "sysusers" table from "master"
    > mssql "SELECT * FROM sysusers\\G"
      - Same as above, using tabular format (mysql client like)

ENVIRONMENT:
    * MSSQL_CRED
        mssql's connection credentials
    * MSSQL_BASE
        mssql's default database to use

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys
import time

from api import plugin
from api import server
from api import environ


def load_credentials(raw_creds):
    """Return a dictionnary of credentials
    elements from raw format.
    """
    result = {}
    result['USER'] = raw_creds[:raw_creds.find('@')]
    result['HOST'] = raw_creds[raw_creds.find('@')+1:]
    result['PASS'] = ''
    if '*' in raw_creds:
        result['HOST'] = raw_creds[raw_creds.find('@')+1:raw_creds.find('*')]
        result['PASS'] = raw_creds[raw_creds.find('*')+1:]
    return result

def sql_str_repr(row):
    return "NULL" if row is None else str(row)

if len(plugin.argv) < 2:
    sys.exit(plugin.help)


# `mssql connect <USERNAME>@<HOSTNAME> [-p <PASSWORD>]`
# Connect to a mssql server with credentials.
# This comment creates or updates the MSSQL_CRED
# environment variable.
if plugin.argv[1].lower() == "connect":
    if len(plugin.argv) < 3:
        sys.exit(plugin.help)
    if plugin.argv[2].count('@') != 1:
        sys.exit("[-] Invalid connection credentials")
    raw_creds = plugin.argv[2]
    if len(plugin.argv) > 3:
        if plugin.argv[3] == "-p":
            password = ' '.join(plugin.argv[4:])
            raw_creds += '*' + password
    creds = load_credentials(raw_creds)
    payload = server.payload.Payload("connect.php")
    payload.update(creds)
    payload.send()
    if "MSSQL_CRED" not in environ:
        environ["MSSQL_CRED"] = ""
    if raw_creds != environ["MSSQL_CRED"]:
        if "MSSQL_BASE" in environ:
            del environ["MSSQL_BASE"]
        environ["MSSQL_CRED"] = raw_creds

    msg = ("[*] SUCCESS: Access granted for user"
           " '%s'@'%s' (using password: %s)")
    msg %= creds["USER"], creds["HOST"], ['YES', 'NO'][not creds['PASS']]
    print(msg)
    sys.exit(0)

# check and load MSSQL_CRED environment variable
if "MSSQL_CRED" not in environ:
    sys.exit("[-] Not connected to any server, use `mssql connect` before")
creds = load_credentials(environ["MSSQL_CRED"])

# format last mssql token correctly
plugin.argv[-1] = plugin.argv[-1].strip().rstrip(';').strip()
if plugin.argv[-1] == "":
    del plugin.argv[-1]


# `mssql use <DATABASE>`
# Select a default database for further mssql queries.
if plugin.argv[1].lower() == "use":
    if len(plugin.argv) != 3:
        sys.exit(plugin.help)
    # prepare and send payload
    payload = server.payload.Payload("setdb.php")
    payload.update(creds)
    payload["BASE"] = plugin.argv[2]
    payload.send()
    # update MSSQL_BASE and exit properly
    environ["MSSQL_BASE"] = plugin.argv[2]
    print("[*] Database changed")
    sys.exit(0)


# `mssql "<SQL COMMAND>"`
# Run an SQL command.
sql_query = " ".join(plugin.argv[1:]).rstrip(';').strip()
if sql_query.endswith('\\G'):
    sql_query = sql_query[:-2].strip()
    display_mode = "line"
else:
    display_mode = "column"
# prepare and send payload
payload = server.payload.Payload("payload.php")
payload.update(creds)
payload["QUERY"] = sql_query
if "MSSQL_BASE" in environ:
    payload["BASE"] = environ["MSSQL_BASE"]
start_time = time.time()
response = payload.send()
end_time = time.time()

elapsed_time = "(%s sec)" % str(round(end_time - start_time, 2))
query_type = response[0]
affected_rows = response[1]
plural = '' if affected_rows == 1 else 's'

# Query type: SET
if query_type == "SET":
    msg = "[*] Query OK, %d row%s affected %s"
    print(msg % (affected_rows, plural, elapsed_time))
    sys.exit(0)

# Query type: GET
if affected_rows == 0:
    sys.exit("[*] Empty set %s" % elapsed_time)

fields = response[2][0]
rows = response[2][1:]

if display_mode == "line":
    field_space = len(max(fields, key=len))
    fields = [(' ' * (field_space - len(x))) + x for x in fields]
    header = "*************************** %d. row ***************************"
    i = 1
    for row in rows:
        print(header % i)
        j = 0
        for field in fields:
            print("%s: %s" % (field, sql_str_repr(row[j])))
            j += 1
        i += 1

elif display_mode == "column":
    columns = [[str(field)] for field in fields]
    for row in rows:
        for i in range(len(fields)):
            columns[i].append(sql_str_repr(row[i]))
    cols_len = [len(max(column, key=len)) for column in columns]
    delimiter = '+-' + ('-+-'.join(['-' * i for i in cols_len])) + '-+'
    for row_no in range(len(columns[0])):
        row = []
        for field_no in range(len(fields)):
            value = columns[field_no][row_no]
            fill = ' ' * (cols_len[field_no] - len(columns[field_no][row_no]))
            row.append(value + fill)
        if row_no < 2:
            print(delimiter)
        print('| ' + (' | '.join(row)) + ' |')
    print(delimiter)

msg = "%s row%s in set %s"
print(msg % (affected_rows, plural, elapsed_time))
sys.exit(0)
