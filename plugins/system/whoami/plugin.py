"""Print effective userid

SYNOPSIS:
    whoami

DESCRIPTION:
    Print the user name associated with current remote
    server access rights.

    * PASSIVE PLUGIN:
    No requests are sent to server, as current user
    is known by $USER environment variable (`env USER`);

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

from api import environ

print(environ['USER'])
