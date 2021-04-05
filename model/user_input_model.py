import re
import socket
from ipaddress import IPv4Address

# from controller.user_input_controller import parse_user_arguments
from scapy.all import *
from scapy.layers.inet import IP, ICMP

from model.constants import MIN_PORT_NUMBER, MAX_PORT_NUMBER, DEFAULT_TIMEOUT, DEFAULT_THREADS, DEFAULT_OUTPUT, \
    DEFAULT_SOUND
from model.scans.tcp.connect_scan import connect_scan
from model.scans.tcp.syn_scan import syn_scan
from model.scans.tcp.xmas_scan import xmas_scan
from model.scans.udp.udp import udp_setup

valid_ports = []


class UserInputModel:

    def __init__(self, target: str, ports: [int], scan_type: str, **kwargs):
        """Constructor check if the user input is valid and set default settings if none are given by the user"""

        self.target = target
        self.ports = ports
        self.scan_type = scan_type
        self.timeout = kwargs.get("to", DEFAULT_TIMEOUT)
        self.threading = kwargs.get("th", DEFAULT_THREADS)
        self.output = kwargs.get("o", DEFAULT_OUTPUT)
        self.sound = kwargs.get("s", DEFAULT_SOUND)

    @staticmethod
    def check_ip(userinput):
        """Check if a valid ip address has been given"""
        ping_host(userinput)  # check if target is up else stop scan

        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", userinput):  # Check if a hostname has been given
            ip = socket.gethostbyname(userinput)  # Change hostname to ip address
            print(f"input {userinput} has been resolved to ip: {ip}")
            try:
                IPv4Address(ip)
                return ip
            except ValueError as errorCode:
                return print(errorCode)

        try:
            IPv4Address(userinput)
            return userinput
        except ValueError as errorCode:
            return print(errorCode)

    @staticmethod
    def check_port(ports):
        """Check if valid ports have been given"""

        if ports is None:
            ports = list(range(1, 1001))  # Assign the first 1000 ports if no port has been given

        if type(ports) is not list:  # Convert a single integer to an integer list with 1 value
            ports = [int(ports)]

        ports = [int(i) for i in ports]  # change CLI String input into a list of integers

        for port in ports:
            if port in range(MIN_PORT_NUMBER, MAX_PORT_NUMBER):
                valid_ports.append(port)
                print(f"port {port} has been added")
            else:
                print("No valid port number has been given. \n"
                      "Make sure the portnumber is not smaller then 1 and larger then 65535.")
                exit(1)

        valid_ports.sort()
        return valid_ports

    @staticmethod
    def check_port_range(ports):
        """Check if a valid port range has been given"""

        for port in ports:
            if port in range(MIN_PORT_NUMBER, MAX_PORT_NUMBER):
                valid_ports.append(port)
            else:
                print(f"Make sure the port range is between {MIN_PORT_NUMBER} and {MAX_PORT_NUMBER}")
                return None

        print(f"total of {len(valid_ports)} ports will be scanned \n"
              f"Starting at port {valid_ports[0]} ending at port {valid_ports[-1]} ")

        valid_ports.sort()
        return valid_ports

    @staticmethod
    def check_remaining_options(remaining_options):
        """Check if the remaining options are valid input"""

    pass

    @staticmethod
    def start_scan(ip, ports, scan_type):
        """Start user specified scan method"""

        if scan_type == "tc":
            connect_scan(ip, ports)
        elif scan_type == "ts":
            syn_scan(ip, ports)
        elif scan_type == "tx":
            xmas_scan(ip, ports)
        elif scan_type == "us":
            udp_setup(ip, ports)


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
