import sys
sys.path.append("..")
import socks
import socket

PY3K = sys.version_info[0] == 3

if PY3K:
    import urllib.request as urllib2
else:
    import sockshandler
    import urllib2

def raw_HTTP_request():
    req = "GET /ip HTTP/1.1\r\n"
    req += "Host: ifconfig.me\r\n"
    req += "User-Agent: Mozilla\r\n"
    req += "Accept: text/html\r\n"
    req += "\r\n"
    return req.encode()

def socket_HTTP_test():
    s = socks.socksocket()
    s.set_proxy(socks.HTTP, "127.0.0.1", 8081)
    s.connect(("ifconfig.me", 80))
    s.sendall(raw_HTTP_request())
    status = s.recv(2048).splitlines()[0]
    assert status.startswith(b"HTTP/1.1 200")

def socket_SOCKS4_test():
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS4, "127.0.0.1", 1080)
    s.connect(("ifconfig.me", 80))
    s.sendall(raw_HTTP_request())
    status = s.recv(2048).splitlines()[0]
    assert status.startswith(b"HTTP/1.1 200")

def socket_SOCKS5_test():
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, "127.0.0.1", 1081)
    s.connect(("ifconfig.me", 80))
    s.sendall(raw_HTTP_request())
    status = s.recv(2048).splitlines()[0]
    assert status.startswith(b"HTTP/1.1 200")

def SOCKS5_connect_timeout_test():
    s = socks.socksocket()
    s.settimeout(0.0001)
    s.set_proxy(socks.SOCKS5, "8.8.8.8", 80)
    try:
        s.connect(("ifconfig.me", 80))
    except socks.ProxyConnectionError as e:
        assert str(e.socket_err) == "timed out"

def SOCKS5_timeout_test():
    s = socks.socksocket()
    s.settimeout(0.0001)
    s.set_proxy(socks.SOCKS5, "127.0.0.1", 1081)
    try:
        s.connect(("ifconfig.me", 4444))
    except socks.GeneralProxyError as e:
        assert str(e.socket_err) == "timed out"


def socket_SOCKS5_auth_test():
    # TODO: add support for this test. Will need a better SOCKS5 server.
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, "127.0.0.1", 1081, username="a", password="b")
    s.connect(("ifconfig.me", 80))
    s.sendall(raw_HTTP_request())
    status = s.recv(2048).splitlines()[0]
    assert status.startswith(b"HTTP/1.1 200")

def socket_HTTP_IP_test():
    s = socks.socksocket()
    s.set_proxy(socks.HTTP, "127.0.0.1", 8081)
    s.connect(("133.242.129.236", 80))
    s.sendall(raw_HTTP_request())
    status = s.recv(2048).splitlines()[0]
    assert status.startswith(b"HTTP/1.1 200")

def socket_SOCKS4_IP_test():
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS4, "127.0.0.1", 1080)
    s.connect(("133.242.129.236", 80))
    s.sendall(raw_HTTP_request())
    status = s.recv(2048).splitlines()[0]
    assert status.startswith(b"HTTP/1.1 200")

def socket_SOCKS5_IP_test():
    s = socks.socksocket()
    s.set_proxy(socks.SOCKS5, "127.0.0.1", 1081)
    s.connect(("133.242.129.236", 80))
    s.sendall(raw_HTTP_request())
    status = s.recv(2048).splitlines()[0]
    assert status.startswith(b"HTTP/1.1 200")

def urllib2_HTTP_test():
    socks.set_default_proxy(socks.HTTP, "127.0.0.1", 8081)
    socks.wrap_module(urllib2)
    status = urllib2.urlopen("http://ifconfig.me/ip").getcode()
    assert status == 200

def urllib2_SOCKS5_test():
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1081)
    socks.wrap_module(urllib2)
    status = urllib2.urlopen("http://ifconfig.me/ip").getcode()
    assert status == 200

def urllib2_handler_HTTP_test():
    opener = urllib2.build_opener(sockshandler.SocksiPyHandler(socks.HTTP, "127.0.0.1", 8081))
    status = opener.open("http://ifconfig.me/ip").getcode()
    assert status == 200

def urllib2_handler_SOCKS5_test():
    opener = urllib2.build_opener(sockshandler.SocksiPyHandler(socks.SOCKS5, "127.0.0.1", 1081))
    status = opener.open("http://ifconfig.me/ip").getcode()
    assert status == 200

def global_override_HTTP_test():
    socks.set_default_proxy(socks.HTTP, "127.0.0.1", 8081)
    good = socket.socket
    socket.socket = socks.socksocket
    status = urllib2.urlopen("http://ifconfig.me/ip").getcode()
    socket.socket = good
    assert status == 200

def global_override_SOCKS5_test():
    default_proxy = (socks.SOCKS5, "127.0.0.1", 1081)
    socks.set_default_proxy(*default_proxy)
    good = socket.socket
    socket.socket = socks.socksocket
    status = urllib2.urlopen("http://ifconfig.me/ip").getcode()
    socket.socket = good
    assert status == 200
    assert socks.get_default_proxy()[1].decode() == default_proxy[1]

def bail_early_with_ipv6_test():
    sock = socks.socksocket()
    ipv6_tuple = addr, port, flowinfo, scopeid = "::1", 1234, 0, 0
    try:
        sock.connect(ipv6_tuple)
    except socket.error:
        return
    else:
        assert False, "was expecting"

def main():
    print("Running tests...")
    socket_HTTP_test()
    print("1/13")
    socket_SOCKS4_test()
    print("2/13")
    socket_SOCKS5_test()
    print("3/13")
    if not PY3K:
        urllib2_handler_HTTP_test()
        print("3.33/13")
        urllib2_handler_SOCKS5_test()
        print("3.66/13")
    socket_HTTP_IP_test()
    print("4/13")
    socket_SOCKS4_IP_test()
    print("5/13")
    socket_SOCKS5_IP_test()
    print("6/13")
    SOCKS5_connect_timeout_test()
    print("7/13")
    SOCKS5_timeout_test()
    print("8/13")
    urllib2_HTTP_test()
    print("9/13")
    urllib2_SOCKS5_test()
    print("10/13")
    global_override_HTTP_test()
    print("11/13")
    global_override_SOCKS5_test()
    print("12/13")
    bail_early_with_ipv6_test()
    print("13/13")
    print("All tests ran successfully")


if __name__ == "__main__":
    main()
