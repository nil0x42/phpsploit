"""A client for MySQL databases

SYNOPSIS:
    mysql connect <USERNAME>@<HOSTNAME> [-p <PASSWORD>]
    mysql show [databases|tables]
    mysql use <DATABASE>
    mysql "<SQL COMMAND>"

DESCRIPTION:
    The mysql plugin tries to simulate the standard mysql
    client.
    - The "connect" argument, used to estabilish a connection
    with the remote mysql server, acts writing a MYSQL_CRED
    environment variable in case of success, this variable is
    automatically used as credentials for next mysql commands.
    - The "use" argument can be used to select a default
    database to explicitly use for next mysql queries, writing
    it into the MYSQL_BASE environment variable.
    - Any other argument string is considered as a single mysql
    query, execpt for ending "\G" strings, which ask to use
    tabular format display mode.

WARNING:
    Considering the PhpSploit's input parser, commands which
    contain quotes, semicolons, and other chars that could be
    interpreted by the framework MUST be enquoted to be
    interpreted as a single argument. For example:
      > run echo 'foo bar' > /tmp/foobar; cat /etc/passwd
    In this case, quotes and semicolons will be interpreted by
    the framwework, so the correct syntax is:
      > run "echo 'foo bar' > /tmp/foobar; cat /etc/passwd"

EXAMPLES:
    > mysql connect root@10.0.0.100 -p god123
      - Connect to 10.0.0.100 as "root" with password "god123"
    > mysql show databases
      - Print the databases list (mysql client like)
    > mysql use information_schema
      - Use the "information_schema" database as default one
    > mysql SELECT * FROM schemata
      - Print the whole schemata table from information_schema
    > mysql "SELECT * FROM schemata\G"
      - Same as above, using tabular format (mysql client like)

ENVIRONMENT:
    * MYSQL_CRED
        Mysql's connection credentials
    * MYSQL_BASE
        Mysql's default database to use

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import time

clock = time.time()

api.isshell()

if self.argc < 2:
    api.exit(self.help)

def getCreds(s):
    r = dict()
    r['USER'] = s[:s.find('@')]
    r['HOST'] = s[s.find('@')+1:]
    r['PASS'] = ''
    if '*' in s:
        r['HOST'] = s[s.find('@')+1:s.find('*')]
        r['PASS'] = s[s.find('*')+1:]
    return(r)

# CONNECT
if self.argv[1].lower() == 'connect':
    if self.argc < 3:
        api.exit(self.help)
    if self.argv[2].count('@') != 1:
        api.exit(P_err+'Invalid connection credentials')
    rawCreds = self.argv[2]
    if self.argc > 3:
        if self.argv[3] == '-p':
            rawCreds+= '*'+(' '.join(self.argv[4:]))

    creds = getCreds(rawCreds)
    http.send(creds, 'connect')

    if http.error:
        api.exit(P_err+http.error)

    if 'MYSQL_CRED' not in api.env:
        api.env['MYSQL_CRED'] = ''
    if rawCreds != api.env['MYSQL_CRED']:
        try: del api.env['MYSQL_BASE']
        except: pass
        api.env['MYSQL_CRED'] = rawCreds

    success = P_inf+"SUCCESS: Access granted for user '%s'@'%s' (using password: %s)"
    api.exit(success % (creds['USER'],creds['HOST'],['YES','NO'][not creds['PASS']]))

if not 'MYSQL_CRED' in api.env:
    api.exit(P_err+"Not connected to any server, use the 'connect' argument")

query = getCreds(api.env['MYSQL_CRED'])

self.argv[-1] = self.argv[-1].strip().rstrip(';').strip()
if not self.argv[-1]: del self.argv[-1]
self.argc = len(self.argv)

# USE
if self.argv[1].lower() == 'use':
    if self.argc != 3:
        api.exit(self.help)
    query['BASE'] = self.argv[2]
    http.send(query, 'setdb')

    if http.error:
        api.exit(P_err+http.error)

    api.env['MYSQL_BASE'] = query['BASE']
    api.exit(P_inf+'Database changed')


# MYSQL QUERIES
if 'MYSQL_BASE' in api.env:
    query['BASE'] = api.env['MYSQL_BASE']

#query['QUERY'] = ' '.join([x.replace(' ','\\ ').replace("\\'",'\'').replace('\\"','\"') for x in self.argv[1:]])
query['QUERY'] = self.args.strip().rstrip(';').strip()

showtype = 'column'
if query['QUERY'].endswith('\\G'):
    query['QUERY'] = query['QUERY'][:-2].strip()
    showtype = 'line'


http.send(query)

if http.error:
    api.exit(P_err+http.error)

clock  = '(%s sec)' % str(round(time.time()-clock,2))+P_NL
num    = str(http.response[1])
plural = ['','s'][num!='1']

# SET QUERIES
if http.response[0] == 'set':
    api.exit(P_inf+'Query OK, %s row%s affected %s' % (num,plural,clock))

# GET QUERIES
if num == '0':
    api.exit(P_inf+'Empty set'+clock)

fields = http.response[2][0]
rows   = http.response[2][1:]

if showtype == 'line':
    fieldSpace = len(max(fields, key=len))
    fields = [(' '*(fieldSpace-len(x)))+x for x in fields]
    i=1
    for row in rows:
        print ('*'*27)+' '+str(i)+'. row '+('*'*27)
        i2 = 0
        for f in fields:
            print f+': '+str(row[i2])
            i2+=1
        i+=1

elif showtype=='column':
    columns = [[x] for x in fields]
    for row in rows:
        for x in range(len(fields)):
            columns[x].append(str(row[x]))
    colsLen = [len(max(x, key=len)) for x in columns]

    separator = '+-'+('-+-'.join(['-'*x for x in colsLen]))+'-+'

    for rowno in range(len(columns[0])):
        row = list()
        for x in range(len(fields)):
            row.append(columns[x][rowno]+(' '*(colsLen[x]-len(columns[x][rowno]))))
        if rowno < 2: print separator
        print '| '+(' | '.join(row))+' |'
    print separator


print '%s row%s in set %s' % (num,plural,clock)
