"""Phpsploit requests and tunnel exceptions
"""
__all__ = ["BuildError", "RequestError", "ResponseError"]


class TunnelException(Exception):
    """Parent class for tunnel exception types
    """


class BuildError(TunnelException):
    """Tunnel request builder exception

    This exception is raised by the tunnel handler if
    something during the request crafting process fails.

    Used by the tunnel.handler.Request().Build() method.
    """


class RequestError(TunnelException):
    """Tunnel request sender exception

    This exception is raised by the tunnel handler if
    something fails while sending phpsploit requests.

    Used by the tunnel.handler.Request.Send() method.
    """


class ResponseError(TunnelException):
    """Tunnel payload dumper exception

    This exception is raised by the tunnel handler if
    the process of payload response extraction within
    the HTTP response fails.

    Used by the tunnel.handler.Request.Read() method.
    """
