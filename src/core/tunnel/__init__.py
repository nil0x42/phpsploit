"""Phpsploit remote tunnel manager.

Usage:
>>> from core import tunnel
>>> if not tunnel:
>>>     tunnel.open()
>>>     tunnel.send("a php payload")
>>> else:
>>>     tunnel.close()
"""
__all__ = ["tunnel"]

from core import session
import ui.input
import ui.color

from . import handler
from . import connector
from . import payload


class Tunnel:
    """Phpsploit remote tunnel manager
    """

    def __init__(self):
        self.socket = None
        self.hostname = None
        self.active = False
        self.payload = payload

    def __bool__(self):
        return self.active

    def open(self):
        """open a new remote connection to TARGET"""
        if self.active:
            raise ValueError("cannot open() an active tunnel")
        socket = connector.Request()
        if socket.open():
            # handler for environment reset if needed
            if {"ADDR", "HOST"}.issubset(session.Env):
                tmp_session = session.deepcopy()
                tmp_session.Env.clear()
                tmp_session.Env.update(socket.environ)
                if session.Env.signature() != tmp_session.Env.signature():
                    ui.color.diff(session.Env, tmp_session.Env)
                    print()

                    question = ("TARGET server have changed, are you "
                                "sure you want to reset environment "
                                "as shown above ?")
                    if ui.input.Expect(False)(question):
                        print("[-] %s (%s): Exploitation aborted"
                              % (tmp_session.Env.ADDR, tmp_session.Env.HOST))
                        self.close()
                        return False
                    print("[*] Environment correctly reset")

            session.Env.update(socket.environ)
            self.socket = socket
            self.hostname = socket.socket.hostname
            print("[*] Shell obtained by PHP (%s -> %s)\n"
                  % (session.Env.CLIENT_ADDR,
                     session.Env.ADDR))
            print("Connected to %s server (%s)"
                  % (session.Env.PLATFORM.capitalize(),
                     session.Env.HOST))
            print("running PHP %s on %s"
                  % (session.Env.PHP_VERSION,
                     session.Env.HTTP_SOFTWARE))
            self.active = True
            return True

        return False

    def close(self):
        """close tunnel"""
        self.active = False
        return True

    def send(self, raw_payload):
        """run a payload on remote server"""
        if not self.active:
            raise ValueError("cannot send() payload: tunnel is not active")
        if not self.socket:
            raise ValueError("cannot send() payload: tunnel has no socket")
        # request = handler.Request()
        request = handler.new_request()
        request.open(raw_payload)
        return request

    def has_been_active(self):
        """check whether this tunnel has already been open() in the past"""
        return bool(self.hostname)

    @staticmethod
    def get_raw_requests():
        """get raw requests data from previously sent payload"""
        return handler.get_raw_requests()


# instanciate main phpsploit tunnel as core.tunnel
tunnel = Tunnel()
