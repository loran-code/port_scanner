import socket
import re
from datetime import datetime


def udp_setup(userinput, timeout):
    """Resolve hostname into an IP address and setup an UDP connection"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", userinput):  # Check if a hostname has been given
        ip = socket.gethostbyname(userinput)
        print(f"input {userinput} has been resolved to ip: {ip}")
        return sock, ip

    return sock, userinput  # Return socket setup and ip address
