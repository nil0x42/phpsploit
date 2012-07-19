
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

# get request cmd
commands+= [' '.join([x.replace(' ','\\ ') for x in self.argv[1:]])]


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
