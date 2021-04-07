import socket
import sys
import threading
from datetime import datetime
from queue import Queue

import colorama
from colorama import Fore

from model.scan_output import save_scan_info_to_file
from model.scans.banner_grab import active_banner_grab
from model.scans.scan_utilities import finish_scan_info, start_scan_info
from model.scans.tcp.tcp import tcp_setup
from model.sqlite_database import save_scan_info_to_database

colorama.init()  # initialize color options
queue = Queue()  #
print_lock = threading.Lock()  #


def connect_scan(scan_data_object):
    """connect scan - creates a 3-way handshake(SYN, SYN ACK, ACK) connection with the target"""
    ip = scan_data_object.target
    ports = scan_data_object.ports
    timeout = scan_data_object.timeout
    threads = scan_data_object.threads
    write_output_to_file = scan_data_object.output_to_file
    save_output_in_database = scan_data_object.save_to_database
    sound = scan_data_object.sound

    open_ports = []
    banner_info = []

    sock = tcp_setup(timeout)  # Setup TCP socket
    tick = start_scan_info(ip, "connect scan")

    try:
        port_counter = 0
        for port in ports:
            try:
                result = sock.connect_ex((ip, port))
                if result == 0:  # The error indicator is 0 if the operation succeeded
                    with print_lock:
                        print(f"Port {port} -" + Fore.GREEN + " Open" + Fore.RESET)
                        banner = active_banner_grab(sock)
                        sock.close()

                        open_ports.append(port)  # add open port to list
                        banner_info.append(banner)  # add corresponding banner to list

                        port_counter += 1

            except KeyboardInterrupt:
                print("[*] User canceled scan")
                sys.exit()

        if port_counter == 0:
            print(f"No open ports have been found")

    except KeyboardInterrupt:
        print("[*] User canceled scan")
        sys.exit()
    except socket.gaierror:
        print('[!] Hostname could not be resolved. Exiting')
        sys.exit()
    except socket.error:
        print("[!] Could not connect to server")
        sys.exit()
    finally:
        sock.close()

    # open_ports = list(zip(open_ports, banner_info))
    # print(open_ports)
    # print(type(open_ports))
    now = datetime.now()
    scan_output = {
        'date time': str(now.strftime("%d-%m-%Y %H:%M")),
        'ip': ip,
        'scan type': "connect scan",
        'scanned ports': ports,
        'open ports': [{
            'port': open_ports,
            'banner': banner_info
        },
        ],
    }

    if write_output_to_file:
        save_scan_info_to_file(scan_output)

    if save_output_in_database:
        save_scan_info_to_database(scan_output)

    finish_scan_info(port_counter, ports, tick, sound)

# t1 = threading.Thread(target=connect_scan)
# t2 = threading.Thread(target=connect_scan)
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
# def worker():
#     while True:
#         worker = queue.get()
#         connect_scan(worker)
#         queue.task_done()
#
#
# def threader(threads, ports):
#     for x in range(threads):
#         thread = threading.Thread(target=worker())
#         thread.daemon = True
#         thread.start()
#
#     for worker in range(ports):
#         queue.put(worker)
#
#     queue.join()
