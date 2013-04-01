"""Copy a file between two remote paths

SYNOPSIS:
    cp [-f] <REMOTE-FILE> <REMOTE-DESTINATION>

OPTIONS:
    -f      Overwrite destination without confirmation if it
            already exists.

DESCRIPTION:
    A basic GNU's 'cp' tool simulation, which acts copying the
    file given as first argument, to the location defined by
    second argument.
    The file to copy must be at least readable, and the
    destination can be a file path, or a directory path.
    - In the case the destination is a directory, the file will
    be copied into it keeping it's original file name.
    - Unless the '-f' option has been set, the copy process
    aborts if the detination file already exists, and asks for
    an confirmation to overwrite the file.

    NOTE: Unlike the standard GNU's 'cp' tool, this plugin can
    not copy more than one file at the time.

EXAMPLES:
    > cp -f exploit.php ../images/archive/IMG0043.PHP
      - Copy an exploit to a stealth location, force copy.
    > cp \\Bach\\LOG\\ex191213.zip C:\\intepub\\wwwroot\\x.zip
      - Copy this interesting file to a web accessible path.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import os, base64

if self.argc not in [3,4]:
    api.exit(self.help)

force = 0
arg1,arg2,arglen = [1,2,self.argc]
if self.argv[1] == '-f':
    force = 1
    arg1,arg2,arglen = [2,3,self.argc-1]

if arglen != 3:
    api.exit(self.help)

src_absPath = rpath.abspath(self.argv[arg1])
dst_absPath = rpath.abspath(self.argv[arg2])

query = {'SOURCE'      : src_absPath,
         'DESTINATION' : dst_absPath,
         'FORCE'       : force}

http.send(query)

errs = {'src_noexists': 'No such file or directory for source',
        'src_notafile': 'Source path is not a file',
        'src_noread':   'Source read permission denied',
        'dst_noexists': 'No such file or directory for destination',
        'dst_notafile': 'Destination path is not a file',
        'dst_nowrite':  'Destination path write permission denied',
        'dst_exists':   'Destination already exists, use the -f argument to force overwrite'}

if http.error in errs:
    api.exit(P_err+self.name+': %1: '+errs[http.error], http.response)


response,destination = http.response

if response == 'ok':
    api.exit(P_inf+'Copy complete: %s -> %s' % (src_absPath, destination))

else:
    api.exit('Unknow error: '+str(http.response))
