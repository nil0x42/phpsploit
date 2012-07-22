from functions import *
import os, sys, pickle

class load():
    errors = {1: 'Permision denied',
              2: 'Bad file content'}

    def __init__(self, sessionFile):
        self.exists  = 0
        self.content = ""
        self.check(sessionFile)

    def check(self, sessionFile):
        if os.path.isfile(sessionFile):
            self.filename = sessionFile
            self.getFile(self.filename)

    def getFile(self, filePath):
        try: rawData = open(filePath).read()
        except: self.getError(1)
        try: self.content = pickle.loads(rawData)
        except: self.getError(2)
        self.exists = 1

    def getError(self, errCode):
        errorMsg = 'Error loading '+quot(self.filename)+': '
        errorVal = self.errors[errCode]
        sys.exit(errorMsg+errorVal)


def save(session, filepath):
    print P_inf+'Saving current session...'

    if not filepath:
        if 'SAVEFILE' in session['SET']:
            filepath = session['SET']['SAVEFILE']
        else:
            filepath = session['SET']['SAVEPATH']

    if not os.sep in filepath:
        filepath = getpath(session['SET']['SAVEPATH'], filepath).name

    filepath = os.path.abspath(filepath)

    if os.path.isdir(filepath):
        filepath = getpath(filepath, 'phpsploit.session').name

    if os.path.exists(filepath):
        query = 'File %s already exists, overwrite it ?' % quot(filepath)
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

