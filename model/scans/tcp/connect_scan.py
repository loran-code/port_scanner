import socket
import sys
import colorama
from colorama import Fore

from model.scans.banner_grab import grab_banner
from model.scans.tcp.tcp import finish_scan_info, start_scan_info, tcp_setup

colorama.init()


def connect_scan(ip, ports):
    """connect scan - creates a 3-way handshake(SYN, SYN ACK, ACK) connection with the target"""

    port_counter = 0
    sock, ip = tcp_setup(ip)  # Setup TCP socket and get the IP that will be scanned
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