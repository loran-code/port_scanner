import re
import socket
import sys
from datetime import datetime
import colorama
from colorama import Fore

from model.banner_grab import grab_banner

colorama.init()


def tcp_setup(userinput):
    """Resolve hostname into an IP address and setup a TCP connection"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # socket.setdefaulttimeout(5)
    sock.settimeout(5)

    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", userinput):  # Check if a hostname has been given
        ip = socket.gethostbyname(userinput)
        print(f"input {userinput} has been resolved to ip: {ip}")
        return sock, ip

    return sock, userinput  # Return connection setup and ip address


def connect_scan(ip, ports):
    """connect scan"""
    port_counter = 0
    sock, ip = tcp_setup(ip)  # Setup TCP socket and get IP for scanning
    tick = start_scan_info(ip)

    try:
        for port in ports:
            result = sock.connect_ex((ip, port))
            if result == 0:  # The error indicator is 0 if the operation succeeded
                port_counter += 1
                print(f"Port {port} -" + Fore.GREEN + " Open" + Fore.RESET)
                grab_banner(sock)

        if port_counter == 0:
            print(f"No open ports have been found")

    except KeyboardInterrupt:
        print("User has canceled the scan")
        sys.exit()
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

    finish_scan_info(port_counter, ports, tick)


def xmas_scan(ip, ports):
    """syn scan"""
    port_counter = 0
    sock, ip = tcp_setup(ip)  # Setup TCP socket
    tick = start_scan_info(ip)

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

    finish_scan_info(port_counter, ports, tick)


def syn_scan(ip, ports):
    """syn scan"""
    port_counter = 0
    sock, ip = tcp_setup(ip)  # Setup TCP socket
    tick = start_scan_info(ip)

    try:
        for port in ports:
            result = sock.connect_ex((ip, port))
            if result == 0:
                port_counter += 1
                print(f"Port {port} - Open")

    except KeyboardInterrupt:
        print("User has canceled the scan")
        sys.exit()
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    except socket.error:
        print("Couldn't connect to server")
        sys.exit()

    finish_scan_info(port_counter, ports, tick)


def start_scan_info(ip):
    """Print starting header about the scan that is being run"""

    tick = datetime.now()
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print(f"Scanning target: {ip}")
    print(f"Scan started at: {tick}")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print("")

    return tick


def finish_scan_info(port_counter, ports, tick):
    """Print closing footer about the scan that is being run"""
    tock = datetime.now()
    scan_time = tock - tick
    print("")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print(f"total of {port_counter} port(s) open out of the {len(ports)} port(s) scanned")
    print(f"Scan completed in: {scan_time}")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")

# class TCP:
#
#     # todo add scan method parameters
#     def __init__(self, ip, ports):
#         self.ip = ip
#         self.ports = ports
