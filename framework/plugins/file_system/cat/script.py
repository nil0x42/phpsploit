import base64

if self.argc != 2:
    api.exit(self.help)

relPath = self.argv[1]
absPath = rpath.abspath(relPath)

if relPath.endswith(rpath.separator):
    api.exit(self.help)

http.send({'FILE' : absPath})

errs = {'noexists': 'No such file or directory',
        'notafile': 'Not a file',
        'noread':   'Permission denied'}

if http.error in errs:
    api.exit(P_err+'%s: %s: %s' % (self.name, absPath, errs[http.error]))

print base64.b64decode(http.response)
