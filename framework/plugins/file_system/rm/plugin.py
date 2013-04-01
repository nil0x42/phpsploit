"""Remove a file

SYNOPSIS:
    rm <REMOTE FILE>

DESCRIPTION:
    Remove the given REMOTE FILE from remote server, or print
    concerned errors in case of insufficient permissions or
    bad file path.

    NOTE: Unlike the GNU's 'rm' coreutils command, this plugin
    only supports a single file as argument.

EXAMPLES:
    > rm pdfs/r57.php
      - Remove the ./pdfs/r75.php file from remote server

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

if self.argc not in [2,3]:
    api.exit(self.help)

recurse = 0

if self.argv[1] == '-r':
    if self.argc == 2:
        api.exit(self.help)
    recurse = 1
    relPath = self.argv[2]
else:
    if len(self.argv) == 3:
        api.exit(self.help)
    relPath = self.argv[1]

absPath  = rpath.abspath(relPath)
dirname  = rpath.dirname(absPath)
basename = rpath.basename(absPath)

query = {'FILE' : absPath}

if recurse:
    api.exit(P_err+"Recursive remote is not available yet !")

else:
    http.send(query, 'single')

    errs = {'noexists': 'No such file or directory',
            'notafile': 'Not a file',
            'noright':  'Permission denied'}

    if http.error in errs:
        api.exit(P_err+self.name+': Impossible to delete %s: %s' % (quot(absPath), errs[http.error]))

    if http.response != 'ok': api.exit('Unknow error: '+str(http.response))
