from ipaddress import IPv4Address

from model.constants import MIN_PORT_NUMBER, MAX_PORT_NUMBER, DEFAULT_TIMEOUT, DEFAULT_THREADS, DEFAULT_OUTPUT, \
    DEFAULT_SOUND

valid_ports = []


def check_user_input(target: str, ports: [int], **kwargs):
    """Check if the user input is valid and set default settings if none are given by the user"""
    kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
    kwargs.setdefault("threading", DEFAULT_THREADS)
    kwargs.setdefault("output", DEFAULT_OUTPUT)
    kwargs.setdefault("sound", DEFAULT_SOUND)


def check_port(ports):
    """Check if valid ports has been given"""

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
            print("No valid port number has been given")

    valid_ports.sort()
    return valid_ports


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


def check_ip(ip):
    """Check if a valid ip address has been given"""

    try:
        IPv4Address(ip)
        return print(f"target: {ip}")
    except ValueError as errorCode:
        return print(errorCode)


def check_scan_options(flags):
    """Check if valid scan options has been given"""

    pass
