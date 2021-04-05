import socket
import sys


def active_banner_grab(banner):
    try:
        banner = banner.recv(1024).decode("utf-8")
        print(f"    {banner}\n")
    except socket.gaierror:
        print('Hostname could not be resolved. Exiting')
        sys.exit()
    except socket.error:
        print("Couldn't connect to server")
        sys.exit()


def passive_banner_grab(target, port):
    # todo passive banner grab
    # telnet target port
    # nc -v target port
    # curl -s -I target | grep -e "Server: "
    # https: // securitytrails.com / blog / banner - grabbing
    pass
