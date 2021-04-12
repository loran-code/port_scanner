import socket


def tcp_setup(timeout):
    """setup TCP connection"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    return sock
