"""Phpsploit remote tunnel manager.

Usage:

>>> from core import tunnel
>>> if not tunnel:
>>>     tunnel.open()
>>>     tunnel.send("a php payload")
>>> else:
>>>     tunnel.close()

"""

from core import session
import ui.input

from . import handler
from . import connector
from . import payload


class Tunnel:

    def __init__(self):
        self.socket = None
        self.hostname = None
        self.active = False
        self.payload = payload

    def __bool__(self):
        return self.active

    def open(self):
        assert not self.active
        socket = connector.Request()
        if socket.open():
            # handler for environment reset if needed
            if self.socket:
                old_hostname = self.socket.socket.hostname
                new_hostname = socket.socket.hostname
                if old_hostname != new_hostname:
                    question = ("TARGET hostname has changed, wish "
                            "you reset environment ? (recommended)")
                    if ui.input.Expect(True)(question):
                        session.Env.clear()
                        print("[*] Environment correctly flushed")
                    else:
                        print("[-] Keeping previous environment")

            session.Env.update(socket.environ)
            self.socket = socket
            self.hostname = socket.socket.hostname
            print("[*] Shell obtained by PHP (%s -> %s:%s)"
                    % (session.Env.CLIENT_ADDR, session.Env.ADDR,
                        session.Env.PORT))
            print()
            print("Connected to %s server (%s)"
                    % (session.Env.PLATFORM.capitalize(), session.Env.HOST))
            print("running PHP %s on %s"
                    % (session.Env.PHP_VERSION, session.Env.HTTP_SOFTWARE))
            self.active = True
            return True

        return False

    def close(self):
        self.active = False
        return True

    def send(self, raw_payload):
        assert self.active
        assert self.socket
        # request = handler.Request()
        request = handler.new_request()
        request.open(raw_payload)
        return request

    def get_raw_requests(self):
        return handler.global_raw_requests

    def has_been_active(self):
        return bool(self.hostname)


# instanciate main phpsploit tunnel as core.tunnel
tunnel = Tunnel()
