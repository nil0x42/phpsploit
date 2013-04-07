"""List directory contents

SYNOPSIS:
    ls [<REMOTE PATH>]

DESCRIPTION:
    List the files in given remote directory path
    - If the given element is not an accessible directory, the
    payload automatically considers the path's basename as a
    regex pattern, it allows to list files which match a
    specific pattern only, for example: "ls /tmp/*.txt", will
    list only .txt files.
    - Ending the argument string with a path separator (for
    example, '/tmp/' instead of '/tmp') explicitly indicates
    that the given path is the exact directory location you
    want to list, so it disables the pattern feature mentionned
    above.

WARNING:
    The 'ls' plugin gives permission informations about each
    listed file, in unix drwxrwxrwx mode. If the permission
    informations are not available, then the payload tries to
    provide basic permission informations in drwx mode, which
    indicates the file rights relative to the current user.

EXAMPLES:
    > ls
      - List any element in the current directory
    > ls ~
      - List any element in the user's home directory
    > ls ..
      - List the path above the current working directory
    > ls D:\\*.ini
      - List any element in D:\\ whose names end with '.ini'

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

if self.argc > 2:
    api.exit(self.help)

if self.argc == 1: relPath = rpath.cwd
else:              relPath = self.argv[1]

absPath = rpath.abspath(relPath)

query = {'TARGET' : absPath, 'PARSE' : 1}

if absPath == rpath.home or relPath.endswith(rpath.separator):
    query['PARSE'] = 0

http.send(query)

errs = {'nodir':   '%1: No such file or directory',
        'noright': '%1: Permission denied',
        'nomatch': '%1: No such elements matching '+quot('%2')}

if http.error in errs:
    api.exit(P_err+self.name+': '+errs[http.error] , http.response)

target,regex,lines = http.response

data = {}

if [x for x in lines if x[2]+x[3]!='??']:
    data['keys'] = ["Mode","Owner","Group","Size","Last Modified","Name"]
    data['data'] = [[x[0],x[2],x[3],x[4],x[5],x[6]] for x in lines]
else:
    data['keys'] = ["Mode","Size","Last Modified","Name"]
    data['data'] = [[x[1],x[4],x[5],x[6]] for x in lines]

data['sep'] = "    "
data['sort'] = len(data['keys'])-1

title = "Listing: "+target
if regex: title+= " (matching "+regex+")"

print ''
print title
print '='*len(title)
print ''
print api.columnize(data)
print ''

