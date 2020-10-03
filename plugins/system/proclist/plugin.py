"""Get process list

SYNOPSIS:
    proclist

DESCRIPTION:
    List processes on remote server.
    * On WINDOWS, the plugin gets results from:
        <? win32_ps_list_procs(); ?>
    * On LINUX, the following is used:
        <? system("ps -a"); ?>
        (OPSEC-unsafe !)

EXAMPLES:
    > cloudcredgrab
      - look for all cloud credentials in all user directories
    > cloudcredgrab -u www aws
      - look for AWS credentials in www's user files

AUTHOR:
    Jose <https://twitter.com/jnazario>
"""

import sys

from api import plugin
from api import server

import plugin_args

if len(plugin.argv) != 1:
    sys.exit(plugin.help)

# options are not used for the moment...
opt = plugin_args.parse(plugin.argv[1:])

payload = server.payload.Payload("payload.php")

result = payload.send()

print("%5s %40s" % ("PID", "INFORMATION"))
print("%5s %40s" % ("---", "-----------"))
for elem in results:
    pid, info = elem.split(" ", 1)
    print("%5s %40s" % (pid, info.strip()))
