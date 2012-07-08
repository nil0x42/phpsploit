
if self.argc > 2:
    api.exit(self.help)

if self.argc == 1: relPath = rpath.cwd
else:              relPath = self.argv[1]

absPath = rpath.abspath(relPath)

query = {'TARGET' : absPath, 'PARSE' : 1}

if absPath == rpath.home or relPath.endswith(rpath.separator):
    query['PARSE'] = 0

http.send(query)

errs = {'nodir':   '%1: No such file or directory',
        'noright': '%1: Permission denied',
        'nomatch': '%1: No such elements matching '+quot('%2')}

if http.error in errs:
    api.exit(P_err+self.name+': '+errs[http.error] , http.response)

target,regex,lines = http.response

data = {}

if [x for x in lines if x[2]+x[3]!='??']:
    data['keys'] = ["Mode","Owner","Group","Size","Last Modified","Name"]
    data['data'] = [[x[0],x[2],x[3],x[4],x[5],x[6]] for x in lines]
else:
    data['keys'] = ["Mode","Size","Last Modified","Name"]
    data['data'] = [[x[1],x[4],x[5],x[6]] for x in lines]

data['sep'] = "    "
data['sort'] = len(data['keys'])-1

title = "Listing: "+target
if regex: title+= " (matching "+regex+")"

print ''
print title
print '='*len(title)
print ''
print api.columnize(data)
print ''

