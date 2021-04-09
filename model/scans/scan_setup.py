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

    try:
        return ping(ip, count=2, timeout=2).success()

    except ConnectionError as errorCode:  # If ping fails
        print(errorCode)
        print(f"{Fore.RED}[!]{Fore.RESET} Could not ping target")
        print(f"{Fore.RED}[!]{Fore.RESET} Exiting")
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
        pass
        # asyncio.run(play_knocking_sound())

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
