"""List directory contents

SYNOPSIS:
    ls [<REMOTE PATH>] ...

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

    NOTE: If the plugin receives multiple arguments, each
    one will be listed in the given order.

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
    > ls .. /home
      - List the path above the current working directory
      - After that, list the '/home' directory.
    > ls D:\\*.ini
      - List any element in D:\\ whose names end with '.ini'

MAINTAINERS:
    nil0x42 <http://goo.gl/kb2wf>
    Wannes Rombouts <https://github.com/wapiflapi>
"""

import sys

from ui.color import colorize, decolorize

from api import plugin
from api import server
from api import environ

status = 0

def abort(msg):
    global status
    status |= 1
    print("[-] %s: %s" % (plugin.name, msg))

for path in plugin.argv[1:] or [environ['PWD']]:

    absolute_path = server.path.abspath(path)

    lister = server.payload.Payload("payload.php")
    lister['TARGET'] = absolute_path
    lister['SEPARATOR'] = server.path.separator(absolute_path)

    lister['PARSE'] = 1
    if absolute_path == environ['HOME'] or path.endswith(environ['PATH_SEP']):
        lister['PARSE'] = 0

    try:
        response = lister.send()
    except server.payload.PayloadError as e:
        if e.args[0] == 'nodir':
            abort("cannot access %s: No such file or directory." % (path))
        if e.args[0] == 'noright':
            abort("cannot open %s: Permission denied." % (path))
        if e.args[0] == 'nomatch':
            abort("cannot find %s: No matching elements." % (path))

        # try with the next item
        continue
    target, regex, lines = response[0], response[1], response[2]

    # if at least one owner/group is not '?', use unix-like formatter
    if any((x[2] + x[3]) != '??' for x in lines):
        rows_hdr = ["Mode", "Owner", "Group", "Size", "Last Modified", "Name"]
        rows = ([l[0], l[2], l[3], l[4], l[5], l[6]] for l in lines)
    # otherwise, use windows-like formatter
    else:
        rows_hdr = ["Mode", "Size", "Last Modified", "Name"]
        rows = ([x[1], x[4], x[5], x[6]] for x in lines)

    # format rows the right way
    rows = sorted(rows, key=(lambda elem: elem[-1]))
    rows.insert(0, rows_hdr)
    rows.insert(1, [("-" * len(elem)) for elem in rows_hdr])

    # format and display output title
    header = "Listing: %s" % target
    if regex:
        header += " (matching r'%s')" % colorize("%White", regex)
    print("\n" + header + "\n" + ("=" * len(decolorize(header))) + "\n")

    widths = [max(map(len, col)) for col in zip(*rows)]
    for i, row in enumerate(rows):
        if i > 0:
            if row[0].startswith('d'):
                row[-1] = colorize("%BoldBlue", row[-1])
            elif not row[0].startswith('-'):
                row[-1] = colorize("%BoldPink", row[-1])
        print("  ".join((val.ljust(width) for val, width in zip(row, widths))))

    print()

sys.exit(status)
