import sys
from functions import *

class reply:
    def __init__(self, core):
        self.cmdname = core['cmd']['name']

    def getLineReply(self, query):
        sys.stdout.write(query)
        response = raw_input(' ')
        return(response)

    def isyes(self, query):
        query = P_inf+self.cmdname+': '+query+' [y/n] :'
        response = ''
        while response not in ['y','n']:
            try: response = self.getLineReply(query).lower()
            except: pass
        if response == 'y': return(True)
        return(False)
