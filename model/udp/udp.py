import socket
from datetime import datetime


def udp_setup():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


class UDP:

    # todo add scan method parameters
    def __init__(self, ip, ports):
        self.ip = ip
        self.ports = ports

    def udp_scan(self):
        pass
