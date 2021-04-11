import multiprocessing
import concurrent.futures
from colorama import Fore
from pythonping import ping

from model.repository.sqlite_database import create_db
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
    """Start user specified scan method and database connection"""
    database_connection = scan_data_object.save_to_database
    knock = scan_data_object.knock
    joke = scan_data_object.joke
    scan_type = scan_data_object.scan_type
    threads = scan_data_object.threads

    with concurrent.futures.ProcessPoolExecutor() as executor:

        if database_connection:  # Start up database connection
            f1 = executor.submit(create_db)
        if knock:
            f2 = executor.submit(play_knocking_sound)
        if joke:
            f3 = executor.submit(play_joke)

        if scan_type == "tc":
            f4 = executor.submit(connect_scan(scan_data_object))
        elif scan_type == "ts":
            f4 = executor.submit(syn_scan(scan_data_object))
        elif scan_type == "tx":
            f4 = executor.submit(xmas_scan(scan_data_object))
        elif scan_type == "us":
            f4 = executor.submit(udp_scan(scan_data_object))


