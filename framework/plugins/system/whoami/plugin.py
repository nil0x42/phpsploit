"""Print effective userid

SYNOPSIS:
    whoami

DESCRIPTION:
    Print the user name associated with the current remote
    server access privileges.

    NOTE: This plugin do not sends any http request, since the
    displayed informations are taken from the api.server vars.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

print api.server['user']
