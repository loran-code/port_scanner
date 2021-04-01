#!/usr/bin/python3
# v1.0
# https://github.com/loran-code/port_scanner

import argparse


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
    help_menu()


pass


def banner():
    banner_text = open('utils/banner.txt', 'r').read()
    print(banner_text)


def option_menu():
    pass


def help_menu():
    """Print out the different options/flags"""

parser = argparse.ArgumentParser(description=banner())
parser.add_argument("target IP", help="IP4V Target address")
parser.add_argument("-p ", metavar="", help="Single port e.g. 80")
parser.add_argument("-pl ", metavar="", help="Port list e.g. 21,22,80")
parser.add_argument("-pr ", metavar="", help="Port range e.g. 20-30")
parser.add_argument("-t ", metavar="", type=int, default=2, help="Timeout value (default 2)")
parser.add_argument("-th ", metavar="", type=int, default=1, help="Amount of threads (default 1)")
parser.add_argument("-o ", metavar="json / xml", help="output format")
parser.add_argument("-s ", metavar="", help="Activates sound to inform when a scan has been finished")
args = parser.parse_args()
target = args.target

pass

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n Thank you for knocking, goodbye!")
        quit()


def run():
    pass
