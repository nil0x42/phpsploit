"""Output information about PHP's configuration

SYNOPSIS:
    phpinfo

DESCRIPTION:
    Dump the remote server's phpinfo() data in tabular
    text format.

AUTHOR:
    nil0x42 <http://goo.gl/kb2wf>
"""

import sys

import ui.output
from ui.color import colorize

from api import server


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

phpinfo = server.payload.Payload("payload.php").send()
if not phpinfo:
    sys.exit("Payload failed to dump phpinfo() array")

tty_cols = ui.output.columns()

for category in phpinfo:

    header = " " + ("_" * (tty_cols - 2)) + " "
    header += '|' + (' ' * (tty_cols - 2)) + '|'
    header += '|' + category.center(tty_cols - 2) + '|'
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
