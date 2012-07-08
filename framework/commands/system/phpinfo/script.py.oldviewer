import os

def sanitize(string):
    return string.replace('  ',' ').strip()

def lineify(string, maxlen):
    string = ' '.join(string.splitlines())
    strLen = len(string)
    if not strLen > maxlen:
        return([string+(' '*(maxlen-strLen))])
    words = string.split()
    result = list()
    if [x for x in words if len(x) > maxlen]:
        while len(''.join(result)) != strLen:
            result.append(string[:maxlen])
            string = string[maxlen:]
    else:
        tempStr = ''
        for word in words:
            if len(tempStr+word) > maxlen:
                result.append(tempStr.strip())
                tempStr = ''
            tempStr+= word+' '
        if tempStr:
            result.append(tempStr.strip())
    result = [x+(' '*(maxlen-len(x))) for x in result]
    return(result)

def tablify(vals):
    maxLstLen = len(max(vals, key=len))
    for elem in vals:
        while len(elem) != maxLstLen:
            elem.append(' '*len(elem[0]))
    lines = dict()
    for n in range(maxLstLen):
        lines[n] = list()
    for elem in vals:
        for n in range(maxLstLen):
            lines[n].append(elem[n])
    result = '';
    for n in lines:
        result+= '| '+(' | '.join(lines[n]))+' |'+os.linesep
        footer = '+-'+('-+-'.join(['-'*len(x) for x in lines[n]]))+'-+'
    return(result+footer)


http.send()

phpinfo = http.response
SIZE    = termlen()

if not phpinfo: api.exit('Unknow error')

for category in phpinfo:

    print ''
    print color(34,1)+' '+('_'*(SIZE-2))+' '
    print '|'+(' '*(SIZE-2))+'|'
    print '|'+category.center(SIZE-2)+'|'
    print '|'+('_'*(SIZE-2))+'|'+color(0)

    singles  = list()
    elements = list()

    for name in phpinfo[category]:
        value = phpinfo[category][name]
        name  = sanitize(name)
        if value == None:
            singles.append( name )
        else:
            elements.append( (name,value) )

    if [(n,v) for (n,v) in elements if type(v).__name__ == 'list']:
        old = elements ; elements = list()
        for (n,v) in old:
            n = sanitize(n)
            if type(v).__name__ == 'list':
                lv, mv = sanitize(v[0]) , sanitize(v[1])
            else:
                lv, mv = sanitize(v), sanitize(v)
            elements.append( (n,lv,mv) )

    if elements:
        titles = ['Variable']
        if len(elements[0]) == 2:
            titles+= ['Value']
        else:
            titles+= ['Local Value','Master Value']

        lists = list(); lens = list(); maxLen = SIZE-1
        for n in range(len(elements[0])):
            lst = [x[n] for x in elements]
            lists.append(lst)
            lens.append( max(len(titles[n]),len(max(lst,key=len))) )
            maxLen-= 3

        def allInts(intsLst):
            res = 0
            for i in intsLst:
                res+=i
            return(res)

        if allInts(lens) > maxLen:
            lens[0] = len(max([max(x.split(' '),key=len) for x in lists[0]],key=len))

        for n in range(1,len(lens)):
            lens[n] = (maxLen-lens[0])/(len(lens)-1)

        while allInts(lens) < maxLen:
            lens[-1]+=1

        separator = '+-'; header = '| '
        for n in range(len(lens)):
            separator+= ('-'*(lens[n]))+'-+-'
            header+= color(1)+lineify(titles[n],lens[n])[0]+color(0)+' | '
        separator = separator[:-1]; header = header[:-1]

        print separator
        print header
        print separator

        for line in elements:
            tmp = []
            for n in range(len(lens)):
                tmp.append(lineify(line[n],lens[n]))
            print tablify(tmp)

    for elem in singles:
        if not elements:
            print '+'+('-'*(SIZE-2))+'+'
        print tablify([lineify(elem, SIZE-4)])
print ''
