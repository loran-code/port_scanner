import os
import socket
import sys
import wget


def active_banner_grab(sock):
    try:
        banner = sock.recv(1024).decode("utf-8")
        print(f"    {banner}\n")
        return banner
    except socket.gaierror:
        print("    No banner - Hostname could not be resolved")
    except socket.error:
        print("    No banner - Could not connect")


def passive_banner_grab(target, port):
    # todo passive banner grab
    # test = wget.url(target)
    # print(test)
    # test2 = os.system("wget http://www.domain.com/ -q -S")
    # test3 = os.system(f'curl -s -I {target}:{port}')
    # print(test2)
    # print(test3)
    # telnet target port
    # nc -v target port
    # curl -s -I target | grep -e "Server: "
    # https: // securitytrails.com / blog / banner - grabbing
    pass
