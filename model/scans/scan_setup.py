from scapy.all import *
from scapy.layers.inet import IP, ICMP

from model.scans.tcp.connect_scan import connect_scan
from model.scans.tcp.syn_scan import syn_scan
from model.scans.tcp.xmas_scan import xmas_scan
from model.scans.udp.udp import udp_setup


def ping_host(ip):
    conf.verb = 0  # Hide output
    try:
        ping = sr1(IP(dst=ip) / ICMP())  # Ping the target
        print("\n[*] Target is Up, Beginning Scan...")
    except ConnectionError as errorCode:  # If ping fails
        print(errorCode)
        print("\n[!] Couldn't Ping Target")
        print("[!] Exiting...")
        sys.exit(1)


def start_scan(scan_data_object):
    """Start user specified scan method"""
    scan_data_object = scan_data_object
    scan_type = scan_data_object.scan_type

    if scan_type == "tc":
        connect_scan(scan_data_object)
    elif scan_type == "ts":
        syn_scan(scan_data_object)
    elif scan_type == "tx":
        xmas_scan(scan_data_object)
    elif scan_type == "us":
        udp_setup(scan_data_object)
