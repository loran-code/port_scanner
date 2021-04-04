import socket
import sys


def grab_banner(banner):
    try:
        banner = str(banner.recv(1024))
        banner = banner.replace("b\'", "")
        banner = banner[:-5]
        print(f"    {banner}\n")
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    except socket.error:
        print("Couldn't connect to server")
        sys.exit()
