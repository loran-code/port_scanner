from ipaddress import IPv4Address

from colorama import Fore
from scapy.all import *

from model.constants import MIN_PORT_NUMBER, MAX_PORT_NUMBER
from model.scans.scan_setup import target_is_up

valid_ports = []


class UserInputModel:

    def __init__(self, target: str, ports: [int], scan_type: str, **kwargs):
        """Constructor check if the user input is valid and set default settings if none are given by the user"""
        self.target = target
        self.ports = ports
        self.scan_type = scan_type
        self.timeout = kwargs.get("to")
        self.threads = kwargs.get("th")
        self.output_to_file = kwargs.get("o")
        self.save_to_database = kwargs.get("db")
        self.sound = kwargs.get("s")
        self.knock = kwargs.get("knock")
        self.joke = kwargs.get("joke")

    @staticmethod
    def check_ip(userinput):
        """Check if a valid ip address has been given"""
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", userinput):  # Check if a hostname has been given
            try:
                ip = socket.gethostbyname(userinput)  # Change hostname to ip address
                print(f"{Fore.GREEN}--{Fore.RESET}input \"{userinput}\" has been resolved to IP: {ip}")
            except socket.gaierror as errorCode:
                print(errorCode)
                print("Make sure the given hostname is valid")
                exit()

            if target_is_up(ip):   # check if target is up else stop scan
                try:
                    IPv4Address(ip)  # Check if the IPv4 is valid
                    return ip

                except ValueError as errorCode:
                    return print(errorCode)
            else:
                print(f"[!] Target: {userinput} - {ip} is not up - Stopping scanner")
                exit()

        if target_is_up(userinput):
            try:
                IPv4Address(userinput)
                return userinput

            except ValueError as errorCode:
                return print(errorCode)
        else:
            print(f"[!] Target: {userinput} is not up - Stopping scanner")
            exit()

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
            else:
                print(f"{Fore.RED}--{Fore.RESET}No valid port number has been given. \n"
                      "Make sure the portnumber is not smaller then 1 and larger then 65535.")
                exit()

        valid_ports.sort()

        if len(valid_ports) > 1:
            print(f"{Fore.GREEN}--{Fore.RESET}ports {valid_ports} have been added")
        else:
            print(f"{Fore.GREEN}--{Fore.RESET}scanning port {valid_ports[0]}")

        return valid_ports

    @staticmethod
    def check_port_range(ports):
        """Check if a valid port range has been given and return a list of valid ports"""
        for port in ports:
            if port in range(MIN_PORT_NUMBER, MAX_PORT_NUMBER):
                valid_ports.append(port)
            else:
                print(f"{Fore.RED}--{Fore.RESET}Make sure the port range is between {MIN_PORT_NUMBER} and "
                      f"{MAX_PORT_NUMBER}")
                return None

        print(f"{Fore.GREEN}--{Fore.RESET}Start scan at port {valid_ports[0]} ending at port {valid_ports[-1]}")

        valid_ports.sort()
        return valid_ports