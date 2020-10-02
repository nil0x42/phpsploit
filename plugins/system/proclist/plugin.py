import sys

from api import plugin
from api import server

from ui.color import colorize
import plugin_args

if len(plugin.argv) < 2:
    sys.exit(plugin.help)

opt = plugin_args.parse(plugin.argv[1:])

payload = server.payload.Payload("proclist.php")

result = payload.send()

print("%5s %40s" % ("PID", "INFORMATION"))
print("%5s %40s" % ("---", "-----------"))
for elem in results:
    pid, info = elem.split(" ", 1)
    print("%5s %40s" % (pid, info.strip()))
