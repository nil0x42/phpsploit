#-*- coding: iso-8859-15 -*-
import os, sys, random
from tempfile import gettempdir

TEMP_DIR   = gettempdir()
SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))


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


def write(seq):
    sys.stdout.write(seq)
    sys.stdout.flush()


def sleep_or_press_enter(timeout):
    from signal import signal, alarm, SIGALRM
    def stop(signum, frame): pass
    signal(SIGALRM, stop)
    alarm(timeout)
    try:
        raw_input()
    except KeyboardInterrupt:
        print ''
        raise KeyboardInterrupt
    except:
        print ''
        pass
    alarm(0)


def clear():
    clearCmd = ['clear','cls'][os.name == 'nt']
    os.system(clearCmd)


# send bash colour sequences > color(0,4) == '\033[0,4m'
# USE IT TO KEEP WINDOWS COMPATIBILITY !
def color(*codes):
    result = ''
    if sys.platform.startswith('linux'):
        for code in codes:
            if type(code).__name__ == 'int':
                result+='\033['+str(code)+'m'
    return(result)


# enquote a string
# USE IT TO KEEP WINDOWS COMPATIBILITY !
def quot(string):
    if sys.platform.startswith('linux'):
        return('«'+string+'»')
    return('"'+string+'"')


# get current terminal length
def termlen():
    try: width = int(os.popen('stty size','r').read().split()[1])
    except: width = 79
    return(width)


# split_len('lol',2) -> ['lo','l']
def split_len(seq, length):
    return [seq[i:i+length] for i in range(0, len(seq), length)]


# get bytes number from octets string `octets('1kb') > 1024`
def octets(value):
    try:
        x=int(value)
        return(x)
    except:
        try: value = str(value).lower()
        except: return(0)
        value = value.replace('o','b')
        tab = ['b','k','m','g','t']
        try: i=[value.index(x) for x in value if x in tab][0]
        except: return(0)
        if not i: return(0)
        l=value[i]
        try: n=int(value[:i])
        except: return(0)
        m=1024**(tab.index(l))
        return(n*m)


# used for REQ_INTERVAL setting's syntax
def getinterval(seq):
    seq = seq.strip().replace(' ','').replace(',','.')
    try:
        if not '-' in seq:
            n1,n2 = float(seq),float(seq)
        else:
            n1,n2 = [float(x) for x in seq.split('-')]
        return(random.uniform(n1,n2))
    except:
        return(None)


# get a custom object from a path
class getpath:
    def __init__(self, path, optionalPath=''):
        if os.path.isabs(path) or optionalPath:
            base = os.path.expanduser(path)
            path = optionalPath
        else:
            base = SCRIPT_DIR
        path = os.path.expanduser(path.replace('/',os.sep))
        if path:
            self.name = os.path.join(base, path)
        else:
            self.name = base

    def access(self, permission):
        if   permission == 'w': check = os.W_OK
        elif permission == 'r': check = os.R_OK
        elif permission == 'x': check = os.X_OK
        status = os.access(self.name, check)
        return(status)

    def exists(self):
        return(os.path.exists(self.name))

    def isfile(self):
        return(os.path.isfile(self.name))

    def read(self):
        lines = self.readlines()
        data = P_NL.join(lines)
        return(data)

    def phpcode(self):
        data = self.read().strip()
        if data.startswith('<?php'): data = data[5:]
        elif data.startswith('<?'):  data = data[2:]
        if data.endswith('?>'):      data = data[:-2]
        data = data.strip()
        return('\n'.join([x.strip() for x in data.splitlines() if x.strip() and not x.strip().startswith('//')]))
        #return(data)

    def write(self, data):
        lines = data.splitlines()
        data = P_NL.join(lines)
        open(self.name,'w').write(data)

    def readlines(self):
        data = open(self.name,'r').read()
        lines = data.splitlines()
        return(lines)

    def randline(self):
        lines = self.readlines()
        lines = [x for x in lines if x]
        if not lines:
            lines = ['']
        result = random.choice(lines)
        return(result)


# a stinking function for debugging
def debug(path, data):
    debugPath = 'phpsploit/debug'
    path = debugPath+'/'+path.strip('/')
    path = getpath(TEMP_DIR, path)
    dirName = os.path.dirname(path.name)
    try: os.makedirs(dirName)
    except: pass
    try: path.write(data)
    except: pass


# GLOBALS:
P_err = color(31,01)+'[-]'+color(0)+' '
P_inf = color(34,01)+'[*]'+color(0)+' '

P_NL  = os.linesep
