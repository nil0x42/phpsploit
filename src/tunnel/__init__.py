"""Phpsploit remote tunnel manager.

Usage:

>>> import tunnel
>>> if not tunnel.socket:
>>>     tunnel.open()
>>> else:
>>>     tunnel.close()

"""

from core import session
import ui.input

from . import handler
from . import connector
from . import payload


class Socket:

    def __init__(self):
        self.socket = None
        self.hostname = None
        self.active = False

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
                        session.Env = {}
                        print("[*] Environment correctly flushed")
                    else:
                        print("[-] Keeping previous environment")

            self.socket = socket
            self.hostname = socket.socket.hostname
            self.active = True
            return True

        return False

    def close(self):
        self.active = False
        return True

    def send(self, raw_payload):
        assert self.active
        assert self.socket
        request = handler.Request()
        request.open(raw_payload)
        response = request.read()
        return response


socket = Socket()
