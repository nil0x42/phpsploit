"""Get informations about a file

SYNOPSIS:
    fileinfo <REMOTE FILE>|<REMOTE DIRECTORY>

DESCRIPTION:
    Display real privileges, rights, and owner informations
    about the given remote file or directory path.

    Unless the 'ls' command which just prints system's files
    rights, the fileinfo command really tries to read and write
    to the given path, to get the real privilege iniformations
    on it.
    It also prints the "Last Modified" information, and the
    absolute path of the element.

WARNING:
    Because it physically tries to write to the file, this
    command will alter the "Last Modified" attribute, which may
    decrease stealth in some cases. For this reason, the
    'fileinfo' plugin must be used sparingly !

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

if self.argc != 2:
    api.exit(self.help)

absPath = rpath.abspath(self.argv[1])

http.send({'TARGET' : absPath})

r = http.response

if r['mode'].startswith('u---') and r['size'] == '0':
    api.exit(P_err+self.name+': '+absPath+': No such file or directory')

result = list()

types = {'s' : 'Socket',
         'l' : 'Symbolic Link',
         '-' : 'File',
         'b' : 'Special block',
         'd' : 'Directory',
         'c' : 'Special char',
         'p' : 'FIFO Pipe',
         'u' : 'Unknow'}

result.append(['Type',types[r['type']]])

if 'owner' in r:
    result.append(['Owner', r['owner']])
    result.append(['Group', r['group']])
    result.append(['Mode', r['mode']])

result.append(['Writeable', r['write']])
result.append(['Readable', r['read']])
result.append(['Executable', r['exec']])
result.append(['Last Modified', r['mtime']])

if r['type'] == 'd':
    absPath+=rpath.separator
else:
    result.append(['Size', r['size']])

result.append(['Absolute Path', absPath])

print ('')
print ('File informations')
print ('=================')
print ('')
for x in result:
    print (x[0]+(' '*(15-len(x[0])))+x[1])

print ('')
