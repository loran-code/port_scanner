import socket
import sys
from datetime import datetime


def tcp_setup(ip):
    """Resolve hostname into an IP address and setup a TCP connection"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.setdefaulttimeout(5)
    # sock.settimeout(5)

    hostname_to_ip = socket.gethostbyname(ip)
    print(f"input {ip} has been translated to ip: {hostname_to_ip}")

    return sock, hostname_to_ip


def connect_scan(ip, ports):
    port_counter = 0
    sock, ip = tcp_setup(ip)  # Setup TCP socket
    print(type(sock))
    print(sock)
    print(type(ip))
    print(ip)

    print(60 * "-")
    tick = datetime.now()
    print(f"Scanning target: {ip}")
    print(f"Scanning started at: {tick}")
    print(60 * "-")

    try:
        for port in ports:
            result = sock.connect_ex((ip, port))
            if result == 0:
                port_counter += 1
                print(f"Port {port} - Open")
            # sock.close()

    except KeyboardInterrupt:
        print("User has canceled the scan")
        sys.exit()
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

    tock = datetime.now()
    print(60 * "-")
    scan_time = tock - tick
    print(f"total of {port_counter} port(s) open out of the {len(ports)} port(s) scanned")
    print(f"Scan completed in: {scan_time}")
    print(60 * "-")


def xmas_scan(ip, ports):
    connection = tcp_setup(ip)  # Setup TCP socket


def syn_scan(ip, ports):
    connection = tcp_setup(ip)  # Setup TCP socket

# class TCP:
#
#     # todo add scan method parameters
#     def __init__(self, ip, ports):
#         self.ip = ip
#         self.ports = ports
