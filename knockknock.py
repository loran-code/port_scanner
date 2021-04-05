#!/usr/bin/python3
# v1.0
# https://github.com/loran-code/port_scanner

from controller.user_input_controller import parse_user_arguments
from utils.banner import banner


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
    parse_user_arguments()


def run_app():
    """Starts the gui application"""
    pass


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n Thank you for knocking, bye!")
        quit()
