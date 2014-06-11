"""Phpsploit remote tunnel manager.

Usage:

>>> import tunnel
>>> if not tunnel.socket:
>>>     tunnel.open()
>>> else:
>>>     tunnel.close()

"""

from . import handler
from . import connector
from . import payload

socket = None


def open():
    global socket
    temp_socket = connector.Request()
    # If open() raises no error, use it as new standard socket
    temp_socket.open()
    socket = temp_socket


def close():
    global socket
    socket.close()
    socket = None


def send(raw_payload):
    request = handler.Request()
    request.open(raw_payload)
    response = request.read()
    return response
