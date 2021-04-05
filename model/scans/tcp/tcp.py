import socket
from datetime import datetime
import colorama
from colorama import Fore

colorama.init()


def tcp_setup():
    """Resolve hostname into an IP address and setup a TCP connection"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)

    return sock  # Return socket setup and ip address


def start_scan_info(ip, scan_type):
    """Print starting header about the scan that is being run"""

    tick = datetime.now()
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print(f"Scan type: {scan_type}")
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