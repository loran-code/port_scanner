#!/usr/bin/python3
# v1.0
# https://github.com/loran-code/port_scanner

from controller.user_input_controller import parse_user_arguments
from model.tcp.tcp import connect_scan, xmas_scan, syn_scan

# ip = "45.33.32.156"
ip = "192.168.0.1"
# ip = "scanme.nmap.org"
ports = list(range(1, 1001))


# ports = list(range(80, 85))


def main():
    """
    Get user input
    - type of scan tcp/udp
        - tcp-connect scan
        - tcp-syn scan
        - UDP scan
        - XMAS scan
    - output format json y/n
    - write to sqlite database y/n
        - ip scanned
        - scan type used
        - ports scanned / port range
        - status open/closed
        - date time
        """
    # banner()
    connect_scan(ip, ports)
    # syn_scan(ip, ports)
    # xmas_scan(ip, ports)
    # parse_user_arguments()


def banner():
    """prints pretty banner"""
    banner_text = open('utils/banner.txt', 'r').read()
    print(banner_text)


def run_app():
    """Starts the application"""
    pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n Thank you for knocking, goodbye!")
        quit()
