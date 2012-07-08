import base64, sys
import phpcode.phpserialize
import network.sender
from functions import *

class http:
    queryEncode = 'global $Q,$R;$Q=%s;\n'

    def __init__(self, core):
        self.core      = core
        self.cmdcwd    = core['cmd']['cwd']
        self.separator = core['SERVER']['separator']
        #self.compress  = core['SERVER']['compress']

    def send(self, query=dict(), payloadname='payload'):
        self.error    = None
        self.response = None
        payload = getpath(self.cmdcwd, payloadname+'.php').phpcode()

        query['SEPARATOR'] = self.separator

        phpQuery = self.queryEncode % phpcode.payload.py2phpVar(query)
        payload  = phpQuery+payload

        request = network.sender.Load(self.core)
        request.open(payload)

        if request.error:
            if request.error == 'request':
                print P_err+'Communication with the server impossible'
            if request.error == 'execution':
                print P_err+'Php runtime error'
            sys.exit()

        self.response = request.read()

        if request.response_error:
            self.error    = request.response_error[0]
            self.response = request.response_error[1:]
