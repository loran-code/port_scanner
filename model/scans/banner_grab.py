import socket
from colorama import Fore


def active_banner_grab(sock):
    """Grabs banner from the target if it's available else return 'no banner available'"""
    try:
        banner = sock.recv(1024).decode("utf-8")
        print(f"    {banner}")
        return banner

    except socket.gaierror:
        print(f"    {Fore.RED}No banner{Fore.RESET} - Hostname could not be resolved")
        no_banner = "No banner available"
        return no_banner

    except socket.error:
        print(f"    {Fore.RED}No banner{Fore.RESET} - Could not connect")
        no_banner = "No banner available"
        return no_banner


def passive_banner_grab(target, port):
    # todo passive banner grab
    # test = wget.url(target)
    # os.system("wget http://www.domain.com/ -q -S")
    # os.system(f'curl -s -I {target}:{port}')
    # telnet target port
    # nc -v target port
    # curl -s -I target | grep -e "Server: "
    pass
