if self.argc not in [2,3]:
    api.exit(self.help)

if self.argc == 2:
    relPath = rpath.cwd
    pattern = self.argv[1]
else:
    relPath = self.argv[1]
    pattern = self.argv[2]

absPath  = rpath.abspath(relPath)

if pattern.endswith(rpath.separator):
    api.exit(self.help)

http.send({'DIR' : absPath , 'PATTERN' : pattern})

errs = {'noexists': 'No such file or directory',
        'notadir':  'Not a directory',
        'noright':  'Permission denied',
        'nomatch':  'No such elements matching %s' % quot(pattern)}

if http.error in errs:
    api.exit(P_err+self.name+': %s: %s' % (absPath, errs[http.error]))

data = {"sep"  : "   ",
        "sort" : 2,
        "keys" : ["Mode","Size","Path"],
        "data" : http.response}

number = len(http.response)
title = "Found %s result%s matching %s in %s" % (str(number), ['','s'][number>1], pattern, absPath)

print ''
print title
print '='*len(title)
print ''
print api.columnize(data)
print ''
