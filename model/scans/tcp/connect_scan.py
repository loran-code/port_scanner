import socket
import threading
from datetime import datetime
from colorama import Fore

from model.scan_output import save_scan_info_to_file
from model.scans.banner_grab import active_banner_grab
from model.scans.scan_utilities import finish_scan_info, start_scan_info
from model.scans.tcp.tcp import tcp_setup
from model.repository.sqlite_database import save_scan_info_to_database

print_lock = threading.RLock()  # Required for printing output in consecutive order


def connect_scan(scan_data_object):
    """connect scan - creates a 3-way handshake(SYN, SYN ACK, ACK) connection with the target
    https://nmap.org/book/scan-methods-connect-scan.html"""
    ip = scan_data_object.target
    ports = scan_data_object.ports
    timeout_time = scan_data_object.timeout
    write_output_to_file = scan_data_object.output_to_file
    save_output_in_database = scan_data_object.save_to_database
    # threads = scan_data_object.threads  # Not been implemented yet

    open_ports = []
    banner_info = []
    port_counter = 0

    tick = start_scan_info(ip, "TCP Connect scan")

    try:
        for port in ports:
            try:
                sock = tcp_setup(timeout_time)  # Setup TCP socket
                result = sock.connect_ex((ip, port))
                if result == 0:  # The error indicator is 0 if the operation succeeded
                    with print_lock:
                        print(f"Port {port} - {Fore.GREEN}Open{Fore.RESET}")
                        banner = active_banner_grab(sock)  # Grab banner from open port
                        sock.close()

                        open_ports.append(port)  # add open port to list
                        banner_info.append(banner)  # add corresponding banner to list
                        port_counter += 1

            except KeyboardInterrupt:
                print(f"{Fore.GREEN}[*]{Fore.RESET} User canceled scan - Thank you for knocking, bye!")
                exit()

        if port_counter == 0:
            print(f"No open ports have been found")

    except KeyboardInterrupt:
        print(f"{Fore.GREEN}[*]{Fore.RESET} User canceled scan - Thank you for knocking, bye!")
        exit()
    except socket.gaierror:
        print(f"{Fore.RED}[!]{Fore.RESET} Hostname could not be resolved. Exiting")
        exit()
    except socket.error:
        print(f"{Fore.RED}[!]{Fore.RESET} Could not connect to server")
        exit()
    finally:
        sock.close()

    date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    scan_output = {
        'date time': str(date_time),
        'ip': ip,
        'scan type': "tcp connect scan",
        'scanned ports': ports,
        'open ports': {
            'port number': open_ports,
            'banner': banner_info
        }
    }

    if port_counter > 0:
        if save_output_in_database:
            save_scan_info_to_database(scan_output)

        if write_output_to_file:
            save_scan_info_to_file(scan_output)

    finish_scan_info(port_counter, tick, scan_data_object)