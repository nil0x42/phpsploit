
if self.argc != 2:
    api.exit(self.help)

relPath  = self.argv[1]
absPath  = rpath.abspath(relPath)

http.send({'DIR' : absPath})

errs = {'noexists': 'No such file or directory',
        'notempty': 'The directory is not empty',
        'noright':  'Permission denied',
        'notadir':  'Not a directory'}

if http.error in errs:
    api.exit(P_err+self.name+': Failed to remove %s: %s' % (quot(absPath), errs[http.error]))

if http.response != 'ok': api.exit(P_err+'Unknow error: '+str(http.response))
