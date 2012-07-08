import os, base64

if self.argc not in [3,4]:
    api.exit(self.help)

force = 0
arg1,arg2,arglen = [1,2,self.argc]
if self.argv[1] == '-f':
    force = 1
    arg1,arg2,arglen = [2,3,self.argc-1]

if arglen != 3:
    api.exit(self.help)

src_absPath = rpath.abspath(self.argv[arg1])
dst_absPath = rpath.abspath(self.argv[arg2])

query = {'SOURCE'      : src_absPath,
         'DESTINATION' : dst_absPath,
         'FORCE'       : force}

http.send(query)

errs = {'src_noexists': 'No such file or directory for source',
        'src_notafile': 'Source path is not a file',
        'src_noread':   'Source read permission denied',
        'dst_noexists': 'No such file or directory for destination',
        'dst_notafile': 'Destination path is not a file',
        'dst_nowrite':  'Destination path write permission denied',
        'dst_exists':   'Destination already exists, use the -f argument to force overwrite'}

if http.error in errs:
    api.exit(P_err+self.name+': %1: '+errs[http.error], http.response)


response,destination = http.response

if response == 'ok':
    api.exit(P_inf+'Copy complete: %s -> %s' % (src_absPath, destination))

else:
    api.exit('Unknow error: '+str(http.response))
