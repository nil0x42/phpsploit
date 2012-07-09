import os, base64

if self.argc not in [2,3,4]:
    api.exit(self.help)

force = 0
arg1,arg2,arglen = [1,2,self.argc]
if self.argv[1] == '-f':
    force = 1
    arg1,arg2,arglen = [2,3,self.argc-1]

l_relPath = self.argv[arg1]

relPath = rpath.cwd
if arglen == 3:
    relPath = self.argv[arg2]

absPath    = rpath.abspath(relPath)
l_absPath  = os.path.abspath(l_relPath)
l_basename = os.path.basename(l_absPath)

leave = P_err+self.name+': '+l_absPath+': '

if os.path.exists(l_absPath):
    if os.path.isfile(l_absPath):
        try: data = base64.b64encode(open(l_absPath,'r').read())
        except: api.exit(leave+'Read permission denied')
    else:
        api.exit(leave+'Is not a file')
else:
    api.exit(leave+'No such file or directory')

query = {'TARGET' : absPath,
         'NAME'   : l_basename,
         'DATA'   : data,
         'FORCE'  : force}

for secondTry in range(2):
    if secondTry:
        query['FORCE'] = 1

    http.send(query)

    errs = {'noexists': 'No such remote file or directory',
            'notafile': 'Remote path is not a file',
            'nowrite':  'Remote path write permission denied'}

    if http.error in errs:
        api.exit(P_err+self.name+': %1: '+errs[http.error], http.response)

    response,target = http.response
    if response == 'ok':
        api.exit(P_inf+'Upload complete: %s -> %s' % (l_absPath, target))

    if response == 'exists' and not secondTry:
        if not reply.isyes('Remote destination %s already exists, overwrite it ?' % quot(target)):
            api.exit(P_err+self.name+': File transfer aborted')

    else:
        api.exit('Unknow error: '+str(http.response))
