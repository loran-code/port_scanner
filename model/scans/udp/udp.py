import socket
import re


def udp_setup(scan_data_object):
    """Resolve hostname into an IP address and setup an UDP connection"""
    userinput = scan_data_object.target
    timeout = scan_data_object.timeout

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(timeout)

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", userinput):  # Check if a hostname has been given
        ip = socket.gethostbyname(userinput)
        print(f"input {userinput} has been resolved to ip: {ip}")
        return sock, ip

    return sock, userinput  # Return socket setup and ip address
