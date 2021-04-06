import socket


def tcp_setup():
    """Resolve hostname into an IP address and setup a TCP connection"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    return sock  # Return socket setup and ip address
