#-*- coding: iso-8859-15 -*-
import os, sys, random
from tempfile import gettempdir

# these two vars are required for some of the following functions.
TEMP_DIR   = gettempdir()
SCRIPT_DIR = os.path.abspath(os.path.dirname(sys.argv[0]))


def write(string):
    """Like the print() function, without the ending newline"""
    sys.stdout.write(string)
    sys.stdout.flush()


def sleep_or_press_enter(timeout):
    """This function takes an integer as argument, then it just returns
    once the timeout has expired OR the user has pressed <ENTER>

    """
    from signal import signal, alarm, SIGALRM

    def stop(signum, frame):
        """empty function for compatibility"""
        pass

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


def raw_repr(string):
    """Used by the nocmd and nohelp to print a command in a single
    line, with enquoted decorator when if contains some unprintable chars

    """
    stringRepr = '$%r' %string

    if string != stringRepr[2:-1]:
        string = stringRepr

    return(string)



def color(*colorCodes):
    """returns the shell color string tag corresponding the the
    given integer codes, I.E: color(1,2) -> \033[1m\033[2m

    """
    string = ''
    if sys.platform.startswith('linux'):
        for code in colorCodes:
            string += '\x1b[%sm' %code
    return(string)


def decolorize(colorString):
    """Clears the shell color tags from the given string"""
    from re import sub
    regex = '(\x1b\[\d+?m)'
    clearString = sub(regex, '', colorString)
    return(clearString)


def quot(string):
    """Nicely enquote the given string with «», or with simple
    quotes on windows systems, must be used instead or raw enquoting
    to keep compatibility with microsoft systems

    """
    if sys.platform.startswith('linux'):
        return( '«'+string+'»' )
    return( '"'+string+'"' )


# get current terminal length
def termlen():
    """Get the current terminal's length with the linux's stty size.
    Otherwise, it simply returns 79 as length because it is the minimum

    """
    try:
        sttySize = os.popen('stty size','r').read()
        length = int( sttySize.split()[1] )
    except:
        length = 79
    return(length)


# split_len('phpsploit', 2) -> ['ph', 'ps', 'pl', 'oi', 't']
def split_len(string, length):
    """split the given string into a list() object which contains
    a list of string sequences or 'length' size.
    Example: split_len('phpsploit', 2) -> ['ph', 'ps', 'pl', 'oi', 't']
    """
    result = list()
    for pos in range(0, len(string), length):
        end = pos + length
        newElem = string[pos:end]
        result.append(newElem)
    return(result)


def split_len_color(string, length):
    """same as above, ignoring shell color tags for count"""

    result  = list()
    pot     = ''
    potLen  = 0
    visible = True
    for char in string:
        if potLen == length:
            result.append(pot)
            pot = ''
            potLen = 0
        if char == '\x01':
            visible = False
        pot+=char
        if visible:
            potLen+=1
        if char == '\x02':
            visible = True
    if pot:
        result.append(pot)
    return(result)


def octets(value):
    """Tansform the given bytesize string into an integer,
    i.e: octets('1kb') -> int(1024)

    """
    # simply return the current value if it in an integer
    try:
        return( int(value) )
    except:
        pass
    # or make de proper transformation
    try:
        value = str(value).lower()
    except:
        return(0)

    value = value.replace('o','b') # 'ko' and 'kb' is the same
    byteChars = ['b','k','m','g','t']    # byte prefix values
    # only take the first non int char into account (ko -> k || b -> b)
    try:
        charIndex = [value.index(x) for x in value if x in byteChars][0]
    except:
        return(0)
    if not charIndex:
        return(0)
    char = value[charIndex]
    try:
        baseInt = int( value[:charIndex] )
    except:
        return(0)
    # convert the byte char to an integer multiplicator
    multiplicator = 1024 ** ( byteChars.index(char) )

    return( baseInt*multiplicator )


def getinterval(seq):
    """Used for the REQ_INTERVAL setting's syntax, it takes a string
    like '2-5' as argument and returns a random float between 2 and 5
    It returns None if an error occurs.

    """
    seq = seq.strip().replace(' ','').replace(',','.')
    try:
        if not '-' in seq:
            n1,n2 = float(seq),float(seq)
        else:
            n1,n2 = [float(x) for x in seq.split('-')]

        return( random.uniform(n1,n2) )
    except:
        return(None)


# ask a question
class ask:
    """Ask the given string as a user question that needs to be
    interactively answered. agree() and reject() methods handles
    the boolean questions (yes/no), while the _getreponse()
    retrieves the given response, re-asking while no input has been
    given, and correctly handling keyboard interrupts and Ctrl-D.

    """
    bool_tpl = ' [y/n] : '

    def __init__(self, question):
        self.question = P_inf+question

    def _getresponse(self, choices):
        choices = [x.lower() for x in choices]
        response = None
        while response not in choices:
            try: response = raw_input(self.question).lower()
            except (EOFError, KeyboardInterrupt): print ''
            except: pass
        return(response)

    def _bool_ask(self, default='y'):
        """Ask the given question string, considering 'yes' as default
        when calling the agree() method, or 'no' calling reject() instead
        - The default choice is bolded and considered as the made choice if
        the user press enter without any input.

        """
        hilight = color(1)+default.upper()+color(0)
        tpl = self.bool_tpl.replace(default, hilight)
        self.question+=tpl
        response = self._getresponse(['y','n',''])
        if response == '':
            response = default
        if response == default:
            return(True)
        return(False)

    def agree(self):
        """see the _bool_ask() method"""
        return( self._bool_ask('y') )

    def reject(self):
        """see the _bool_ask() method"""
        return( self._bool_ask('n') )


class getpath:
    """Instantiate a file object, with usefull methods for PhpSploit
    The getpath() class takes one or two file paths as arguments,
    and it determines the wanted file target.
    - When two paths are specified, the first one is considered as the
    base directory, while the second is the relative file.
    - When a single path is given, the PhpSploit's root directory is
    assumed as base directory, while the given argument is considered
    as the target file path.

    Vars:
        name (string):  the file's absolute path

    """
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
        """check if the file has 'permission' (rwx) access rights"""

        if   permission == 'w': check = os.W_OK
        elif permission == 'r': check = os.R_OK
        elif permission == 'x': check = os.X_OK
        status = os.access(self.name, check)
        return(status)

    def exists(self):
        """True if the file exists"""
        return(os.path.exists(self.name))

    def isfile(self):
        """True if file is a regular file"""
        return(os.path.isfile(self.name))

    def isdir(self):
        """True if file is a directory"""
        return(os.path.isdir(self.name))

    def dirname(self):
        """Return the file's directory name (/tmp/x -> /tmp)"""
        return(os.path.dirname(self.name))

    def read(self):
        """Return the file content, eventually replacing the line
        separator (\n) with the system's specific one.

        """
        lines = self.readlines()
        data = P_NL.join(lines)
        return(data)

    def phpcode(self):
        """Return the file's content, removing first the php
        ending and starting tags (<? and ?>).
        - It also removes comment lines, empty lines, and useless
        trailing spaces.
        - '\n' is used as line separator in any case.

        NOTE: multiline comment (/* foo\nbar */) are NOT supported
        an must NOT be used in the PhpSploit framework.

        """
        data = self.read().strip()
        if data.startswith('<?php'): data = data[5:]
        elif data.startswith('<?'):  data = data[2:]
        if data.endswith('?>'):      data = data[:-2]
        data = data.strip()
        result = list()
        for line in data.splitlines():
            line = line.strip()
            if not line.startswith('//'):
                result.append(line)
        return('\n'.join(result))

    def write(self, data):
        """write 'data' to the file. System specific line separator
        is used as newlines, independently of the given data

        """
        lines = data.splitlines()
        data = P_NL.join(lines)
        open(self.name,'w').write(data)

    def readlines(self):
        """Return the file's data lines as a list() object"""
        data = open(self.name,'r').read()
        lines = data.splitlines()
        return(lines)

    def randline(self):
        """Pick-up a random line from the fil data"""
        lines = self.readlines()
        lines = [x for x in lines if x]
        if not lines:
            lines = ['']
        result = random.choice(lines)
        return(result)


# a stinking function for debugging
def debug(path, data):
    """a stinking function for debugging...
    it will be removed some day, it and the 'debug' command, to replace
    them by a real, non sucking debuging mode.

    """
    debugPath = 'phpsploit/debug'
    path = debugPath+'/'+path.strip('/')
    path = getpath(TEMP_DIR, path)
    dirName = os.path.dirname(path.name)
    try: os.makedirs(dirName)
    except: pass
    try: path.write(data)
    except: pass


# These are the global variables, accessible from everywhere
# since an "from function import *" line is used.

P_err = color(31,01)+'[-]'+color(0)+' ' # the error prefix [-]
P_inf = color(34,01)+'[*]'+color(0)+' ' # the info prefix [*]
P_NL  = os.linesep # the system specific newline string

from string import ascii_letters, digits
P_ALNUM = ascii_letters+digits # alphanumeric chars
P_CHARS = P_ALNUM+'_' # commonly accepted chars (alnum + underscore)
