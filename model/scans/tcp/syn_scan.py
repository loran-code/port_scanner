from colorama import Fore
from scapy.all import *
from scapy.layers.inet import IP, TCP
from threading import RLock
from queue import Queue

from model.scan_output import save_scan_info_to_file
from model.scans.scan_utilities import finish_scan_info, start_scan_info
from model.constants import SYNACK
from model.repository.sqlite_database import save_scan_info_to_database

que = Queue()
print_lock = RLock()


def syn_scan(scan_data_object):
    """syn scan - start half-open connection(SYN, SYN ACK, RST) with the target.
    Takes the origin port from the target reply header
    https://nmap.org/book/synscan.html"""

    conf.verb = 0  # Suppress scapy output in terminal

    # Get required variables from object
    ip = scan_data_object.target
    ports = scan_data_object.ports
    timeout = scan_data_object.timeout
    threads = scan_data_object.threads
    write_output_to_file = scan_data_object.output_to_file
    save_output_in_database = scan_data_object.save_to_database

    open_ports = []
    port_counter = 0

    tick = start_scan_info(ip, "TCP SYN scan")

    try:
        for port in ports:
            src_port = RandShort()  # Generate Port Number
            try:
                # Send SYN and receive RST-ACK or SYN-ACK
                syn_ack_pkt = sr1(IP(dst=ip) / TCP(sport=src_port, dport=port, flags="S"), timeout=timeout)

                # Extract flags of received packet
                pkt_flags = syn_ack_pkt.getlayer(TCP).flags

                # Construct RST packet
                rst_pkt = IP(dst=ip) / TCP(sport=src_port, dport=port, flags="R")

                if pkt_flags == SYNACK:  # Cross reference Flags
                    with print_lock:
                        print(f"Port {port} - {Fore.GREEN}Open{Fore.RESET}")
                        send(rst_pkt)  # Send RST packet
                        open_ports.append(port)  # add open port to list
                        port_counter += 1
                else:
                    send(rst_pkt)

            except KeyboardInterrupt:
                src_port = RandShort()
                rst_pkt = IP(dst=ip) / TCP(sport=src_port, dport=port, flags="R")
                send(rst_pkt)
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
        'scan type': "tcp syn scan",
        'scanned ports': ports,
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
