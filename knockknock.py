#!/usr/bin/python3
# v1.0
# https://github.com/loran-code/port_scanner

from controller.user_input_controller import parse_user_arguments


def main():
    """
    Get user input
    - ip address
    - port(s)
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
    banner()
    run_app()
    parse_user_arguments()


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
