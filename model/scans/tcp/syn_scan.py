import colorama
from colorama import Fore
from logging import getLogger, ERROR
from scapy.all import *
from scapy.layers.inet import IP, TCP
from threading import Thread, Lock
from queue import Queue

from model.scans.banner_grab import passive_banner_grab
from model.scans.banner_grab import active_banner_grab
from model.scans.scan_utilities import finish_scan_info, start_scan_info
from model.constants import SYNACK

getLogger("scapy.runtime").setLevel(ERROR)
colorama.init()

que = Queue()
print_lock = Lock()

def syn_scan(scan_data_object):
    """syn scan - start half-open connection(SYN, SYN ACK, RST) with the target.
    Takes the origin port from the target reply header"""

    ip = scan_data_object.target
    ports = scan_data_object.ports
    sound = scan_data_object.sound

    port_counter = 0
    tick = start_scan_info(ip, "syn scan")

    try:
        for port in ports:
            try:
                src_port = RandShort()  # Generate Port Number

                # Send SYN and receive RST-ACK or SYN-ACK
                syn_ack_pkt = sr1(IP(dst=ip) / TCP(sport=src_port, dport=port, flags="S"))

                # Extract flags of received packet
                pkt_flags = syn_ack_pkt.getlayer(TCP).flags

                # Construct RST packet
                rst_pkt = IP(dst=ip) / TCP(sport=src_port, dport=port, flags="R")

                if pkt_flags == SYNACK:  # Cross reference Flags
                    print(f"Port {port} -" + Fore.GREEN + " Open" + Fore.RESET)
                    # passive_banner_grab(ip, port)
                    send(rst_pkt)  # Send RST packet
                    port_counter += 1
                else:
                    send(rst_pkt)

            except KeyboardInterrupt:  # In case the user needs to quit
                src_port = RandShort()
                rst_pkt = IP(dst=ip) / TCP(sport=src_port, dport=port, flags="R")
                send(rst_pkt)
                print("\n[*] User Requested Shutdown...")
                print("[*] Exiting...")
                sys.exit()

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
