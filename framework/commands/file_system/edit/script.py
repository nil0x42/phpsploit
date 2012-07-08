import os, base64

api.needsenv('TEXTEDITOR')

if self.argc != 2:
    api.exit(self.help)

relPath  = self.argv[1]
absPath  = rpath.abspath(relPath)
basename = rpath.basename(absPath)

if relPath.endswith(rpath.separator):
    api.exit(self.help)

query = {'FILE' : absPath}

http.send(query, 'reader')

errs = {'notafile': 'Not a file',
        'noread':   'Read permission denied'}

if http.error in errs:
    api.exit(P_err+'%s: %s: %s' % (self.name, absPath, errs[http.error]))


tmpDir = getpath(api.settings['TMPPATH'], api.randstring(12)+os.sep).name
try: os.mkdir(tmpDir)
except: api.exit(P_err+"Temporary directory creation failed: "+tmpDir)

lAbsPath = tmpDir+basename
content  = ''

if http.response == 'NEWFILE':
    print P_inf+"Creating new file: "+absPath
else:
    content = base64.b64decode(http.response)
    try: open(lAbsPath,'w').write(content)
    except: api.exit(P_err+"Failed to create a local copy of the file at: "+lAbsPath)
    print P_inf+"Opening file: "+absPath

if os.system(api.env['TEXTEDITOR']+' '+lAbsPath):
    print P_err+"Invalid 'TEXTEDITOR' environment variable"

try: newContent = open(lAbsPath,'r').read()
except: api.exit(P_inf+"File creation aborted")

for fl in os.listdir(tmpDir):
    os.remove(tmpDir+fl)
os.rmdir(tmpDir)

if newContent == content:
    if http.response == 'NEWFILE':
        api.exit(P_inf+"File creation aborted")
    api.exit(P_inf+"The file was not modified")

# XXX #
query['CONTENT'] = base64.b64encode(newContent)

http.send(query,'writer')

if http.error == 'nowrite':
    api.exit(P_err+self.name+': '+absPath+': Write permission denied')

if http.response != 'ok':
    api.exit(P_err+self.name+': Unknown error:\n'+str(http.response))

print P_inf+"File correctly written on "+absPath
