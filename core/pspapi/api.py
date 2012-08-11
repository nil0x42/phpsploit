from functions import *
import sys, string, random

class api:
    def __init__(self, core, cmd):
        self.settings = core['SET']
        self.server   = core['SRV']
        self.env      = core['ENV']
        self.cmd      = cmd

        self.currentShell = core['CURRENT_SHELL']

    def exit(self, text='', replaceLst=None):
        if type(replaceLst).__name__ == 'str':
            replaceLst = [replaceLst]
        if type(replaceLst).__name__ == 'list':
            for n in range(len(replaceLst)):
                text = text.replace('%'+str(n+1), replaceLst[n])
        sys.exit(text)

    def isshell(self):
        if self.currentShell:
            if self.cmd['argc'] == 1:
                self.exit()
            elif self.cmd['argc'] == 2:
                args = ' '.join(self.cmd['argv'][1:])
                if args == '?':
                    self.exit(self.cmd['help'])
                if args == 'exit':
                    raise KeyboardInterrupt

    def needsenv(self, name):
        name = name.upper()
        if not name in self.env:
            if name in self.settings:
                self.env[name] = self.settings[name]
            else:
                self.exit(P_err+"Undefined %s, please enable it with the 'env' command" % name)

    def randstring(self, n):
        chars = string.ascii_letters+string.digits
        return(''.join([random.choice(chars) for i in range(0,n)]))

    def columnize(self, dic):
        if set(dic.keys()) != set(['sep','sort','keys','data']): return('error')
        if [x for x in dic['data'] if len(x) != len(dic['keys'])]: return('error')
        try: c=int(dic['sort'])
        except: return('error')
        linesLen = len(dic['data'])
        colsLen  = len(dic['keys'])
        # get max len
        maxLen = [len(x) for x in dic['keys']]
        for line in dic['data']:
            c=0
            while c != colsLen:
                if len(line[c]) > maxLen[c]:maxLen[c]=len(line[c])
                c+=1

        if dic['sep'].isspace():
            if len(dic['sep'].join([' '*x for x in maxLen]))>termlen():
                dic['sep']='  '

        lst = dic['data']
        # sort the lines by dic['sort'] column number
        if dic['sort'] != -1:
            import operator
            lst.sort(key=operator.itemgetter(dic['sort']))
        # print the list
        txt=''; c=0
        # print keys
        while c != colsLen:
            txt+= dic['keys'][c]+dic['sep']+(" "*(maxLen[c]-len(dic['keys'][c])))
            c+=1
        # print '-'
        txt=txt.strip(); txt+='\n'; c=0
        while c != colsLen:
            txt+= ("-"*len(dic['keys'][c]))+dic['sep']+(" "*(maxLen[c]-len(dic['keys'][c])))
            c+=1
        # print data:
        for line in lst:
            txt=txt.strip(); txt+='\n'; c=0
            while c != colsLen:
                txt+= line[c]+dic['sep']+(" "*(maxLen[c]-len(line[c])))
                c+=1
        return(txt.strip())
