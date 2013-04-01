"""Create directory

SYNOPSIS:
    mkdir [-p] <REMOTE DIRECTORY>

OPTIONS:
    -p      No error if existing, make parent directories as
            needed.

DESCRIPTION:
    The 'mkdir' plugin creates the REMOTE DIRECTORY. It reports
    an error if the path already exists, unless the '-p' option
    is given and the path is a directory.

    NOTE: Unlike the GNU's mkdir core util, this plugin only
    supports single directory creation, no multiple path
    arguments are supported, at least for the moment.

EXAMPLES:
    > mkdir includes
      - Create the 'includes' directory from current location
    > mkdir /srv/www/data/img/thumb/
      - Create the 'thumb' directory if it's parent exists
    > mkdir /srv/www/data/img/thumb/
      - Create the 'thumb' direcroty even if parent don't exist

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

if self.argc not in [2,3]:
    api.exit(self.help)

parent = 0

if self.argv[1] == '-p':
    if self.argc == 2:
        api.exit(self.help)
    parent = 1
    relPath = self.argv[2]
else:
    if self.argc == 3:
        api.exit(self.help)
    relPath = self.argv[1]

absPath  = rpath.abspath(relPath)

if parent:
    query = {'ROOT' : rpath.rootdir(absPath), 'ELEMS' : [x for x in absPath.split(rpath.separator)[1:] if x]}
    http.send(query, 'parent')

else:
    query = {'DIR' : absPath}
    http.send(query)

errs = {'exists':   'File exists',
        'noright':  'Permission denied',
        'noexists': 'No such file or directory'}

if http.error in errs:
    api.exit(P_err+self.name+': Error creating '+quot('%1')+': '+errs[http.error], http.response)

if http.response != 'ok': api.exit(P_err+'Unknown error: '+str(http.response))
