from scapy.all import *
from scapy.layers.inet import IP, ICMP
from concurrent.futures import ThreadPoolExecutor
import asyncio

from model.scans.scan_utilities import play_knocking_sound, play_joke
from model.scans.tcp.connect_scan import connect_scan
from model.scans.tcp.syn_scan import syn_scan
from model.scans.tcp.xmas_scan import xmas_scan
from model.scans.udp.udp import udp_setup


def ping_host(ip):
    conf.verb = 0  # Hide output
    try:
        ping = sr1(IP(dst=ip) / ICMP())  # Ping target with ICMP packet
    except ConnectionError as errorCode:  # If ping fails
        print(errorCode)
        print("\n[!] Could not ping target")
        print("[!] Exiting...")
        sys.exit(1)


def start_scan(scan_data_object):
    """Start user specified scan method"""
    scan_type = scan_data_object.scan_type
    knock = scan_data_object.knock
    joke = scan_data_object.joke
    threads = scan_data_object.threads

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
            udp_setup(scan_data_object)
