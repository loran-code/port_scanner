import colorama
from colorama import Fore
from logging import getLogger, ERROR
from scapy.all import *

from model.scans.banner_grab import grab_banner
from model.scans.tcp.tcp import finish_scan_info, start_scan_info, tcp_setup

getLogger("scapy.runtime").setLevel(ERROR)
colorama.init()


def xmas_scan(ip, ports):
    """xmas scan - start """
    """syn scan - start half-open connection(SYN, SYN ACK, RST) with the target.
    Takes the origin port from the target reply header"""

    port_counter = 0
    sock, ip = tcp_setup(ip)  # Setup TCP socket and get the IP that will be scanned
    tick = start_scan_info(ip)

    # try:
    #     srcport = RandShort()  # Generate Port Number
    #     conf.verb = 0  # Hide output
    #     SYNACKpkt = sr1(
    #         IP(dst=target) / TCP(sport=srcport, dport=port, flags="S"))  # Send SYN and recieve RST-ACK or SYN-ACK
    #     pktflags = SYNACKpkt.getlayer(TCP).flags  # Extract flags of recived packet
    #     if pktflags == SYNACK:  # Cross reference Flags
    #         return True  # If open, return true
    #     else:
    #         return False  # If closed, return false
    #     RSTpkt = IP(dst=target) / TCP(sport=srcport, dport=port, flags="R")  # Construct RST packet
    #     send(RSTpkt)  # Send RST packet
    # except KeyboardInterrupt:  # In case the user needs to quit
    #     RSTpkt = IP(dst=target) / TCP(sport=srcport, dport=port, flags="R")  # Built RST packet
    #     send(RSTpkt)  # Send RST packet to whatever port is currently being scanned
    #     print
    #     "\n[*] User Requested Shutdown..."
    #     print
    #     "[*] Exiting..."
    #     sys.exit(1)

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
