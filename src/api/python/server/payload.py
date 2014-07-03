import tunnel
import objects
from core import session
from api import plugin
from datatypes import Path


class Payload(objects.MetaDict):

    # the phpsploit env vars to auto add
    # to $PHPSPLOIT array on php side
    _unherited_env_vars = ["PATH_SEP"]

    _php_vars_template = 'global $PHPSPLOIT;$PHPSPLOIT=%s;\n'

    def __init__(self, filename, **kwargs):
        self.response = None
        for key in self._unherited_env_vars:
            self[key] = session.Env[key]
        for key, value in kwargs.iteritems():
            self[key] = value
        self.payload = Path(plugin.path, filename, mode='fr').phpcode()

    def send(self, **kwargs):
        vars = dict(self)
        for key, value in kwargs.iteritems():
            vars[key] = value
        php_vars = self._php_vars_template % tunnel.payload.py2php(vars)

        result = tunnel.send(php_vars + self.payload)
        if result.response_error:
            raise PayloadError(result.response_error)
        return result.response


class PayloadError(Exception):
    """Exception raised when a send payload returned an __ERROR__ obj"""

    pass
