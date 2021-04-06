import socket


def tcp_setup(timeout):
    """Resolve hostname into an IP address and setup a TCP connection"""

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    return sock
