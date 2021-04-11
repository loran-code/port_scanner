from colorama import Fore
from pythonping import ping
from concurrent.futures import ThreadPoolExecutor
import asyncio

from model.scans.scan_utilities import play_knocking_sound, play_joke
from model.scans.tcp.connect_scan import connect_scan
from model.scans.tcp.syn_scan import syn_scan
from model.scans.tcp.xmas_scan import xmas_scan
from model.scans.udp.udp_scan import udp_scan


def target_is_up(ip):
    """Check if target is up by pinging the given ip address."""

    try:
        target_up = ping(ip, count=2, timeout=2).success()

        if target_up is True:
            return True
        else:
            return valid_input()  # If user wants to continue the scan the value is True

    except ConnectionError as errorCode:  # If ping fails
        print(errorCode)
        print(f"{Fore.RED}[!]{Fore.RESET} Could not ping target")
        print(f"{Fore.RED}[!]{Fore.RESET} Exiting")
        exit()


def valid_input():
    """Check for valid user input. stop scan if user enters "n" continue scan if user enters "y"""

    print("Target does not respond to ping and might be offline.\n Would You like to continue scanning? y/n")
    target_down = ""

    while True:
        try:
            target_down = str(input("> ")).lower()
        except ValueError:
            print("Please Enter \"y\" or \"n\" as input.")
            continue

        else:
            if target_down == "y" or target_down == "n":
                break
            else:
                print("Please Enter \"y\" or \"n\" as input.")

    if target_down == "y":
        return True
    elif target_down == "n":
        print(f"{Fore.GREEN}[*]{Fore.RESET} User canceled scan - Thank you for knocking, bye!")
        exit()


def start_scan(scan_data_object):
    """Start user specified scan method"""
    scan_type = scan_data_object.scan_type
    knock = scan_data_object.knock
    joke = scan_data_object.joke
    threads = scan_data_object.threads

    # asyncio.gather(play_knocking_sound())
    # asyncio.gather(play_joke())
    # asyncio.get_event_loop().is_running()

    # todo multi threaded
    if knock:
        play_knocking_sound()

    # todo multi threaded
    if joke:
        play_joke()

    with ThreadPoolExecutor(max_workers=threads) as executor:

        if scan_type == "tc":
            executor.submit(connect_scan(scan_data_object))
        elif scan_type == "ts":
            syn_scan(scan_data_object)
        elif scan_type == "tx":
            xmas_scan(scan_data_object)
        elif scan_type == "us":
            udp_scan(scan_data_object)