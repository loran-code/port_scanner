#!/usr/bin/python3
# v1.0
# https://github.com/loran-code/port_scanner

from colorama import Fore

from controller.user_input_controller import parse_user_arguments


def main():
    """
    Get user input
    - type of scan tcp/udp
        - UDP scan
        - XMAS scan
    - code information
    - tests
        """
    parse_user_arguments()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print(f"{Fore.GREEN}[*]{Fore.RESET} User canceled scan - Thank you for knocking, bye!")
        quit()
