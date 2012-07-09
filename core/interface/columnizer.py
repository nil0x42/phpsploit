from functions import *

class Make:
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
