
api.isshell()

if self.argc < 2:
    api.exit(self.help)

cmdSep = ";"
if api.server['platform'] == 'win':
    cmdSep = "&"

cmdSep = " "+cmdSep+" "

commands = list()

# patch to view stderr in linux
if api.server['platform'] == 'nix':
    commands+= ['exec 2>&1']

# go to pwd
commands+= ['cd '+rpath.cwd]

# get request cmd
commands+= [' '.join([x.replace(' ','\\ ') for x in self.argv[1:]])]

CMD = cmdSep.join(commands)

http.send({'CMD' : CMD})

print http.response


