import socket
import sys
from datetime import datetime


def tcp_setup(ip, ports):
    """Setup a TCP connection"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    ip = input("Enter an IP address to scan")
    print(f"input entered is {ip}")
    hostname_to_ip = socket.gethostname(ip)
    print(f"input has been translated to {hostname_to_ip}")

    return sock


class TCP:

    def connect_scan(self, ip, ports = [1, 1000]):
        connection = tcp_setup(ip, ports)
        print("Starting scan")
        tick = datetime.now()

        try:
            for port in range(ports):
                result = connection.connect_ex((ip,port))
                if result == 0:
                    print(f"Port {port} --- Open")
                connection.close()

        except KeyboardInterrupt:
            print("User has canceled the scan")
            sys.exit()

        except socket.gaierror:
            print('Hostname could not be resolved. Exiting')
            sys.exit()

        except socket.error:
            print("Couldn't connect to server")
            sys.exit()

        tock = datetime.now()
        print("Scan finished")

        scan_time = tick - tock
        print(f"Scan time: {scan_time}")

    def syn_scan(self):
        pass

    def xmas_scan(self):
        pass
