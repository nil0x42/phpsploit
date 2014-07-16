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

import sys

from api import plugin
from api import server
from api import environ

from ui.color import colorize

for path in plugin.argv[1:] or [environ['PWD']]:

    absolute_path = server.path.abspath(path)


    lister = server.payload.Payload("payload.php")
    lister['TARGET'] = absolute_path
    lister['SEPARATOR'] = "/"

    # TODO: activate or deactivate PARSE?
    # I don't see the point of this, why not remove PARSE altogether?
    lister['PARSE'] = 1

    try:
        response = lister.send()
    except server.payload.PayloadError as e:
        if e.args[0] == 'nodir':
            sys.exit("cannot access %s: No such file or directory." % (path))
        if e.args[0] == 'noright':
            sys.exit("cannot open %s: Permission denied." % (path))
        if e.args[0] == 'nomatch':
            sys.exit("cannot find %s: No matching elements." % (path))

    target, regex, lines = response[0], response[1], response[2]
    lines = [[v for _, v in sorted(line.items())] for _, line in sorted(lines.items())]

    if any(x[2]+x[3] != '??' for x in lines):
        rows = sorted(([l[0],l[2],l[3],l[4],l[5],l[6]] for l in lines), key=lambda x: x[-1])
        rows.insert(0, ["Mode","Owner","Group","Size","Last Modified","Name"])
    else:
        rows = sorted(([x[1],x[4],x[5],x[6]] for x in lines), key=lambda x: x[-1])
        rows.insert(0, ["Mode","Size","Last Modified","Name"])

    print("Listing: %s" % path + (" (matching r'%s')" % regex if regex else ""))

    widths = [max(map(len, col)) for col in zip(*rows)]
    for i, row in enumerate(rows):
        if i > 0:
            if row[0].startswith('d'):
                row[-1] = colorize("%BoldBlue", row[-1])
            elif not row[0].startswith('-'):
                row[-1] = colorize("%BoldPink", row[-1])

        print("  ".join((val.ljust(width) for val, width in zip(row, widths))))
