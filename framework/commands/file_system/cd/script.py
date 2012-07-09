
if self.argc > 2:
    api.exit(self.help)

if self.argc == 1: relPath = rpath.home
else:              relPath = self.argv[1]

absPath = rpath.abspath(relPath)

http.send({'DIR' : absPath})

errs = {'noexists': 'No such file or directory',
        'notadir':  'Not a directory',
        'noright':  'Permission denied'}

if http.error in errs:
    api.exit(P_err+'%s: %s: %s' % (self.name, absPath, errs[http.error]))

if http.response != 'ok':
    api.exit(P_err+'Unknown error:\n'+str(http.response))

api.env['CWD'] = absPath
