from colorama import Fore
from scapy.all import *
from scapy.layers.inet import IP, ICMP, UDP
from threading import RLock
from queue import Queue

from model.scan_output import save_scan_info_to_file
from model.scans.scan_utilities import finish_scan_info, start_scan_info
from model.constants import ICMP_UNREACHABLE_ERROR, ICMP_UNREACHABLE_ERROR_NUMBERS
from model.repository.sqlite_database import save_scan_info_to_database

que = Queue()
print_lock = RLock()


def udp_scan(scan_data_object):
    """udp scan -
    https://nmap.org/book/scan-methods-udp-scan.html"""

    conf.verb = 0  # Suppress scapy output in terminal

    # Get required variables from object
    ip = scan_data_object.target
    ports = scan_data_object.ports
    timeout = scan_data_object.timeout
    threads = scan_data_object.threads
    write_output_to_file = scan_data_object.output_to_file
    save_output_in_database = scan_data_object.save_to_database

    open_ports = []
    filtered_ports = []
    port_counter = 0

    tick = start_scan_info(ip, "UDP scan")

    try:
        for port in ports:
            try:
                response = sr1(IP(dst=ip) / UDP(dport=port), timeout=timeout)  # Save the response of a UDP packet
                # print(response)
                # print(type(response))
                # print(port_counter)
                if str(type(response)) == "<class 'NoneType'>":
                    retransmit = []
                    for count in range(0, 3):
                        retransmit.append(sr1(IP(dst=ip) / UDP(dport=port), timeout=timeout))

                    for i in retransmit:
                        if str(type(response)) != "<class 'NoneType'>":
                            # udp_scan(scan_data_object)
                            with print_lock:
                                print(f"Port {port} - {Fore.GREEN}Open{Fore.RESET} | {Fore.YELLOW}Filtered{Fore.RESET}")
                            port_counter += 1

                elif response.haslayer(UDP):
                    with print_lock:
                        print(f"Port {port} - {Fore.GREEN}Open{Fore.RESET}")
                    open_ports.append(port)
                    port_counter += 1

                elif response.haslayer(ICMP):
                    if int(response.getlayer(ICMP).type) == ICMP_UNREACHABLE_ERROR and int(
                            response.getlayer(ICMP).code) == ICMP_UNREACHABLE_ERROR:
                        pass  # port is closed

                    if int(response.getlayer(ICMP).type) == ICMP_UNREACHABLE_ERROR and int(
                            response.getlayer(ICMP).code) in ICMP_UNREACHABLE_ERROR_NUMBERS:
                        with print_lock:
                            print(f"Port {port} - {Fore.GREEN}Open{Fore.RESET} | {Fore.YELLOW}Filtered{Fore.RESET}")
                        filtered_ports.append(port)
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

    now = datetime.now()
    scan_output = {
        'date time': str(now.strftime("%d-%m-%Y %H:%M")),
        'ip': ip,
        'scan type': "udp scan",
        'scanned ports': ports,
        'filtered ports': {
            'port number': filtered_ports
        },
        'open ports': {
            'port number': open_ports
        }
    }

    if port_counter > 0:
        if save_output_in_database:
            save_scan_info_to_database(scan_output)

        if write_output_to_file:
            save_scan_info_to_file(scan_output)

    finish_scan_info(port_counter, tick, scan_data_object)
