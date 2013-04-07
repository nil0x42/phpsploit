"""Change directory

SYNOPSIS:
    cd <DIRECTORY>

DESCRIPTION:
    Move the PhpSploit's current working directory to the given
    directory location.
    Unlike manually changing the CWD environment variable to
    the wanted location, this plugins directly checks on the
    remote server if the new directory exists and is
    reachable. For those reasons, and the fact that relative
    paths can be specified, the method is a lot more safe
    than manual CWD edition, which must be used only on the
    rare cases you have no choice.

EXAMPLES:
    > cd ..
      - Go to the directory below
    > cd "C:\\Program Files\\"
      - Go to Program Files directory
    > cd ~
      - Move the the user's base directory

ENVIRONMENT:
    * CWD
        The current PhpSploit working directory

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

if self.argc > 2:
    api.exit(self.help)

if self.argc == 1: relPath = rpath.home
else:              relPath = self.argv[1]

absPath = rpath.abspath(relPath)

http.send({'DIR' : absPath})

errs = {'noexists': 'No such file or directory',
        'notadir':  'Not a directory',
        'noright':  'Permission denied'}

if http.error in errs:
    api.exit(P_err+'%s: %s: %s' % (self.name, absPath, errs[http.error]))

if http.response != 'ok':
    api.exit(P_err+'Unknown error:\n'+str(http.response))

api.env['CWD'] = absPath
