import os
import sys
import socket
from colorama import Fore


def active_banner_grab(sock):
    try:
        banner = sock.recv(1024).decode("utf-8")
        print(f"    {banner}")
        return banner
    except socket.gaierror:
        print(f"    {Fore.RED}No banner{Fore.RESET} - Hostname could not be resolved")
    except socket.error:
        print(f"    {Fore.RED}No banner{Fore.RESET} - Could not connect")


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
