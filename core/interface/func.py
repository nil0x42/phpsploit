from functions import *

class fork_stdout(object):
    """this class can replace sys.stdout and writes
    simultaneously to standard output AND specified file
    usage: fork_stdout(altFile)"""
    def __init__(self, file):
        self.file = file
        self.stdout = sys.stdout
        sys.stdout = self

    def __del__(self):
        sys.stdout = self.stdout
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.stdout.write(data)

    def flush(self):
        self.stdout.flush()


# this class is used to format and print env vars or settings output.
class columnize_vars:
    def __init__(self, title, dic):
        self.title     = title
        self.dic       = dic
        self.blacklist = ['']
        self.width     = 0
        self.colors    = 1
        self.color1    = color(37)
        self.color2    = color(0)
        self.separator = '='

    def cutStr(self, string, sep, num):
        if len(string) > num:
            newstr='' ; x=0
            while x != len(string):
                newstr+=string[x] ; x+=1
                if (x)%num == 0: newstr+=sep
            string = newstr
        return(string)

    def write(self):
        # don't treat empty elems
        dic = dict([(x,str(y)) for x,y in self.dic.items() if str(y) not in self.blacklist])
        dic = [(k,dic[k].strip()) for k in sorted(dic.keys())]

        # get longest name
        maxNameLen = 8;
        for name,value in dic:
            if len(name) > maxNameLen: maxNameLen = len(name)

        # get terminal size
        termLen = self.width
        if not termLen:
            termLen = termlen()

        # format values to from dic to varsList
        printvars='' ; x=0 ; _color = [self.color1,self.color2]
        if not self.colors: _color = ['','']
        while x!= len(dic):
            printvars+=_color[x%2]+'    '+dic[x][0]
            printvars+=' '*(maxNameLen-len(dic[x][0])+2)
            printvars+=self.cutStr(dic[x][1],'\n'+(' '*(maxNameLen+6)),termLen-(maxNameLen+6))+'\n'
            x+=1

        print color(0)
        print self.title
        print self.separator*len(self.title)
        print ""
        print "    Variable"+" "*(maxNameLen-6)+"Value"
        print "    --------"+" "*(maxNameLen-6)+"-----"
        print printvars+color(0)



# this function updates the self.CNF['LNK'] dict.
def update_opener(CNF):
    from re      import findall
    from hashlib import md5
    from base64  import b64encode

    # an ugly line to shorten the function
    CNF['LNK']['DOMAIN'] = 'x'

    target = CNF['SET']['TARGET']
    regex  = '^https?://(.+?)(?:$|/)'
    try:    domain = findall(regex, target)[0]
    except: domain = ''
    if domain and len(target)>13:
        CNF['LNK']['URL']    = target
        CNF['LNK']['DOMAIN'] = domain
    else:
        try: del CNF['LNK']['URL']
        except: pass

    # domain hash building
    domain  = CNF['LNK']['DOMAIN']
    md5Val  = md5(domain).hexdigest()
    b64Val  = b64encode(md5Val)
    CNF['LNK']['HASH'] = b64Val[:8]

    # payload generation
    srvhash  = CNF['LNK']['HASH']
    backdoor = CNF['SET']['BACKDOOR']
    passkey  = CNF['SET']['PASSKEY'].upper().replace('-','_')
    rawPayload = backdoor.replace('%%PASSKEY%%',passkey)
    payload    = rawPayload.replace('%%SRVHASH%%',srvhash)
    CNF['LNK']['BACKDOOR'] = payload

    # passkey generation
    CNF['LNK']['PASSKEY'] = CNF['SET']['PASSKEY']
    if CNF['LNK']['PASSKEY'] == "%%SRVHASH%%":
        CNF['LNK']['PASSKEY'] = CNF['LNK']['HASH']

    return(CNF['LNK'])
