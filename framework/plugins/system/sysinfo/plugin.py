"""Print remote server informations

SYNOPSIS:
    sysinfo

DESCRIPTION:
    Display remote server's various informations which have
    been dumped when the connection has been extabilished.

    NOTE: This plugin do not sends any http request, since the
    displayed informations are taken from the api.server vars.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

print ""
print "Server informations"
print "==================="
print ""
print "IP Address        "+api.server['addr']
print "Hostname          "+api.server['host']
print "Operating System  "+api.server['os']
print "Server Software   "+api.server['soft']
print "PHP Version       "+api.server['phpver']
print "Home Directory    "+api.server['home']
print "Web Direcroty     "+api.server['webroot']
print "Username          "+api.server['user']
print ""

