import socket
import sys
import colorama
from colorama import Fore

from model.scans.banner_grab import active_banner_grab
from model.scans.scan_utilities import finish_scan_info, start_scan_info
from model.scans.tcp.tcp import tcp_setup

colorama.init()


def connect_scan(scan_data_object):
    """connect scan - creates a 3-way handshake(SYN, SYN ACK, ACK) connection with the target"""

    ip = scan_data_object.target
    ports = scan_data_object.ports
    sound = scan_data_object.sound

    port_counter = 0
    sock = tcp_setup()  # Setup TCP socket
    tick = start_scan_info(ip, "connect scan")

    try:
        for port in ports:
            result = sock.connect_ex((ip, port))
            if result == 0:  # The error indicator is 0 if the operation succeeded
                port_counter += 1
                print(f"Port {port} -" + Fore.GREEN + " Open" + Fore.RESET)
                active_banner_grab(sock)

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

    finish_scan_info(port_counter, ports, tick, sound)
