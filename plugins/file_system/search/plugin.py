"""Recursively search for files matching pattern

SYNOPSIS:
    search [<BASE DIRECTORY>] <PATTERN>

DESCRIPTION:
    The 'search' plugin recursively searchs for files and
    directories matching PATTERN from the given BASE DIRECTORY.
    - If the BASE DIRECTORY is not specified, the plugin
    sets it's value at the current working directory, it means
    that 'cd /tmp; search *.c' is the same as 'search /tmp *.c'.

EXAMPLES:
    > search /srv/www *sql*
      - List any file whose name contains 'sql' in the web path
    > search *.inc
      - Recursive search of .inc files from current directory

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

if self.argc not in [2,3]:
    api.exit(self.help)

if self.argc == 2:
    relPath = rpath.cwd
    pattern = self.argv[1]
else:
    relPath = self.argv[1]
    pattern = self.argv[2]

absPath  = rpath.abspath(relPath)

if pattern.endswith(rpath.separator):
    api.exit(self.help)

http.send({'DIR' : absPath , 'PATTERN' : pattern})

errs = {'noexists': 'No such file or directory',
        'notadir':  'Not a directory',
        'noright':  'Permission denied',
        'nomatch':  'No such elements matching %s' % quot(pattern)}

if http.error in errs:
    api.exit(P_err+self.name+': %s: %s' % (absPath, errs[http.error]))

data = {"sep"  : "   ",
        "sort" : 2,
        "keys" : ["Mode","Size","Path"],
        "data" : http.response}

number = len(http.response)
title = "Found %s result%s matching %s in %s" % (str(number), ['','s'][number>1], pattern, absPath)

print('')
print(title)
print('='*len(title))
print('')
print(api.columnize(data))
print('')
