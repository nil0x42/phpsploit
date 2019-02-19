"""Output information about PHP's configuration

SYNOPSIS:
    phpinfo [--browser]

OPTIONS:
    --browser
        Display raw phpinfo()'s HTML output in web browser

DESCRIPTION:
    Display the remote server's phpinfo() data in tabular
    text, formatted for the terminal.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys

import ui.output
from ui.color import colorize

from api import plugin
from api import server
import base64
from datatypes import Path

def sanitize(string):
    return string.replace('  ', ' ').strip()


def lineify(string, maxlen):
    string = ' '.join(string.splitlines())
    strLen = len(string)
    if not strLen > maxlen:
        return [string + (' ' * (maxlen - strLen))]
    words = string.split()
    result = []
    if [x for x in words if len(x) > maxlen]:
        while len(''.join(result)) != strLen:
            result.append(string[:maxlen])
            string = string[maxlen:]
    else:
        tempStr = ''
        for word in words:
            if len(tempStr + word) > maxlen:
                result.append(tempStr.strip())
                tempStr = ''
            tempStr += word + ' '
        if tempStr:
            result.append(tempStr.strip())
    return [x + (' ' * (maxlen - len(x))) for x in result]


def tablify(vals):
    maxLstLen = len(max(vals, key=len))
    for elem in vals:
        while len(elem) != maxLstLen:
            elem.append(' ' * len(elem[0]))
    lines = {}
    for n in range(maxLstLen):
        lines[n] = []
    for elem in vals:
        for n in range(maxLstLen):
            lines[n].append(elem[n])
    result = ''
    for n in lines:
        result += '| ' + (' | '.join(lines[n])) + ' |\n'
        footer_fill = [('-' * len(x)) for x in lines[n]]
        footer = '+-' + ('-+-'.join(footer_fill)) + '-+'
    return result + footer


# `phpinfo` without arguments (tabular text output)
if len(plugin.argv) == 1:
    phpinfo = server.payload.Payload("array_format.php").send()
    if not phpinfo:
        sys.exit("Payload failed to dump phpinfo() array")

    tty_cols = ui.output.columns()

    for category in phpinfo:

        header = " " + ("_" * (tty_cols - 2)) + " \n"
        header += '|' + (' ' * (tty_cols - 2)) + '|\n'
        header += '|' + category.center(tty_cols - 2) + '|\n'
        header += '|' + ('_' * (tty_cols - 2)) + '|'
        print(colorize("\n", "%BoldBlue", header))

        singles = []
        elements = []

        for name in phpinfo[category]:
            value = phpinfo[category][name]
            name = sanitize(name)
            if value is None:
                singles.append(name)
            else:
                elements.append((name, value))

        if [(n, v) for (n, v) in elements if isinstance(v, list)]:
            old = elements
            elements = []
            for (n, v) in old:
                n = sanitize(n)
                if isinstance(v, list):
                    lv, mv = sanitize(v[0]), sanitize(v[1])
                else:
                    lv, mv = sanitize(v), sanitize(v)
                elements.append((n, lv, mv))

        if elements:
            titles = ['Variable']
            if len(elements[0]) == 2:
                titles += ['Value']
            else:
                titles += ['Local Value', 'Master Value']

            lists = []
            lens = []
            maxLen = tty_cols - 1
            for n in range(len(elements[0])):
                lst = [x[n] for x in elements]
                lists.append(lst)
                lens.append(max(len(titles[n]), len(max(lst, key=len))))
                maxLen -= 3

            def allInts(intsLst):
                res = 0
                for i in intsLst:
                    res += i
                return res

            if allInts(lens) > maxLen:
                max_of_each = [max(x.split(' '), key=len) for x in lists[0]]
                lens[0] = len(max(max_of_each, key=len))

            for n in range(1, len(lens)):
                lens[n] = int((maxLen - lens[0]) / (len(lens) - 1))

            while allInts(lens) < maxLen:
                lens[-1] += 1

            separator = '+-'
            header = '| '
            for n in range(len(lens)):
                separator += ('-' * (lens[n])) + '-+-'
                header += colorize("%Bold", lineify(titles[n], lens[n])[0]) + ' | '
            separator = separator[:-1]
            header = header[:-1]

            print(separator + "\n" + header + "\n" + separator)

            for line in elements:
                tmp = []
                for n in range(len(lens)):
                    tmp.append(lineify(line[n], lens[n]))
                print(tablify(tmp))

        for elem in singles:
            if not elements:
                print('+' + ('-' * (tty_cols - 2)) + '+')
            print(tablify([lineify(elem, (tty_cols - 4))]))
    print()
# `phpinfo --browser` (view html output in browser)
elif len(plugin.argv) == 2 and plugin.argv[1] == "--browser":
    html_output = server.payload.Payload("html_format.php").send()
    tmp_file = Path(filename="phpinfo.html")
    tmp_file.write(html_output)
    if tmp_file.browse():
        print("[*] Successfully opened %r in browser" % tmp_file)
    else:
        print("[-] Failed to open %r in web browser" % tmp_file)
        print("[-] Try to change BROWSER environment variable")
else:
    sys.exit(plugin.help)
