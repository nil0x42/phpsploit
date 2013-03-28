from functions import *
import os, sys, pickle

class load():
    """this simple class is designed to load a phpsploit session file.
    it takes the target file path string as first argument, and the
    phpsploit core version (CNF['PSCOREVER']) as second argument.

    the self.error must be used as error checker/printer before trying
    to use the self.content variable, which contains the session
    dictionnary

    """
    def __init__(self, path, version):
        self.error  = None
        self.version = version

        status = self.load_file(path)
        if status is not True:
            err_tpl = P_err+"Error loading %s: %s"
            self.error = err_tpl %(path, status)

    def load_file(self, path):
        """fill the "content" variable with session and return True
        if everything is ok, otherwise return specific error string.

        """
        if not os.path.exists(path):
            return("No such file or directory")
        if not os.path.isfile(path):
            return("Not a file")
        try:
            rawData = open(path).read()
        except:
            return("Permission denied")
        try:
            content = pickle.loads(rawData)
        except:
            return("Not a session file")
        try:
            version = int(content['PSCOREVER'])
        except:
            version = 0
        if version != self.version:
            return("Incompatible session version")

        self.content = content
        return(True)



def save(session, filepath=""):
    """this function saves "session" to "filepath".
    when not specified, the SAVEPATH and SAVEFILE
    settings will be used to determine the path to use.

    when the specified filepath is a simple filename, the SAVEPATH
    setting will be used as base dir instead of the current directory;
    this is why if the file name have to be written in the current dir,
    a relative path must be specified, aka: "./phpsploit.session"
    instead of "phpsploit.session"

    the function directly writes output infos/errors, be aware !

    """
    print P_inf+'Saving current session...'

    # set the default filepath when not specified
    if not filepath:
        if 'SAVEFILE' in session['SET']:
            filepath = session['SET']['SAVEFILE']
        else:
            filepath = session['SET']['SAVEPATH']

    # use SAVEPATH as base dir when filename only is specified.
    if not os.sep in filepath:
        filepath = getpath(session['SET']['SAVEPATH'], filepath).name

    filepath = os.path.abspath(filepath)

    if os.path.isdir(filepath):
        filepath = getpath(filepath, 'phpsploit.session').name

    if os.path.exists(filepath):
        query = 'File %s already exists, overwrite it ?' %quot(filepath)
        if ask(query).reject():
            print P_err+'The session was not saved'
            return(0)

    rawSession = pickle.dumps(session)

    try:
        open(filepath,'w').write(rawSession)
        print P_inf+'Session saved in '+filepath
        return(filepath)
    except:
        print P_err+'Writing error on '+filepath

