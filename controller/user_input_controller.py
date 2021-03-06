import argparse

from colorama import Fore

from model.repository.sqlite_database import query_db
from model.scans.scan_setup import start_scan
from model.user_input_model import UserInputModel
from utils.banner import banner


def parse_user_arguments():
    """
    Parse command line input and derive variables
    needed to check for valid input by parsing
    the variables as arguments to other methods
    """
    parser = argparse.ArgumentParser(description=banner())
    parser.add_argument("-t", "-target", metavar="", type=str, help="IP4V address that needs to be scanned")
    parser.add_argument("-p", "-port", metavar="", type=int, help="Single port e.g. 80")
    parser.add_argument("-pl", "-portlist", metavar="", nargs='+', type=int, help="Port list e.g. 22 53 80 443")
    parser.add_argument("-pr", "-portrange", metavar="", nargs='+', type=int, help="Port range e.g. 1 1023 (default)")
    parser.add_argument("-to", "-timeout", metavar="", type=int, default=5, help="Timeout value (default 5)")
    parser.add_argument("-th", "-threading", metavar="", type=int, default=10, help="Amount of threads (default 10)")
    parser.add_argument("-o", "-output", action='store_true', help="Stores scan result in json and xml format")
    parser.add_argument("-db", "-database", action='store_true', help="Stores the scan result into a SQLite repository")
    parser.add_argument("-dbq", "-query", action='store_true', help="Shows stored scans on given ip")
    parser.add_argument("-s", "-sound", action='store_true', help="Activates sound to inform when a scan has been "
                                                                  "finished")
    parser.add_argument("-tc", "-tcpconnect", action='store_true', help="TCP Connect scan (default)")
    parser.add_argument("-ts", "-tcpsync", action='store_true', help="TCP SYN scan")
    parser.add_argument("-tx", "-tcpxmas", action='store_true', help="TCP XMAS scan")
    parser.add_argument("-us", "-udpscan", action='store_true', help="UDP scan")
    parser.add_argument("-knock", action='store_true', help="The real port knocking experience (requires audio)")
    parser.add_argument("-joke", action='store_true', help="Tell a joke (requires audio)")
    args = vars(parser.parse_args())  # Create dictionary from the given command line arguments

    if args.get("dbq"):  # Query database with the last records of given ip
        query_db(args.get("t"))
        quit()

    ip = parse_user_ip_options(args)  # Parse the given ip
    ports = parse_user_port_options(args)  # Parse the given ports
    scan_type = parse_user_scan_options(args)  # Parse the given scan_type
    remaining_options = parse_remaining_options(args)  # Parse the remaining options

    # Create object with the parsed data input
    scan_data_object = UserInputModel(ip, ports, scan_type, **remaining_options)

    # Pass the object to the start scan method
    start_scan(scan_data_object)


def parse_user_ip_options(args):
    """Parse the user input and returns the ip if it's a valid ip"""
    ip = args.get("t")
    return UserInputModel.check_ip(ip)


def parse_user_port_options(args):
    """Parse the user input and returns the ports that will be scanned."""
    if args.get("p") is not None:
        ports = args.get("p")
        return UserInputModel.check_port(ports)

    elif args.get("pl") is not None:
        ports = args.get("pl")
        return UserInputModel.check_port(ports)

    elif args.get("pr") is not None:
        port_range = args.get("pr")

        if len(port_range) < 2 or len(port_range) > 2:
            print(f"{Fore.RED}--{Fore.RESET}Specify a range with 2 integers e.g. -pr / -portrange 20 100")
            exit()

        if port_range[0] > port_range[1]:
            print(
                f"{Fore.RED}--{Fore.RESET}Specify the smallest number before specifying the large number. e.g. -pr / "
                f"-portrange 20 100")
            exit()
        else:
            port_range = range(port_range[0], port_range[1])
            return UserInputModel.check_port_range(port_range)

    else:
        print(f"{Fore.GREEN}--{Fore.RESET}No port range has been specified defaulting to portrange 1-1023")
        return UserInputModel.check_port_range(range(1, 1024))


def parse_remaining_options(args):
    """Parse the user input and return what remaining options have been chosen"""
    remaining_options = {"to": args.get("to"), "th": args.get("th")}

    if args.get("o"):
        remaining_options["o"] = args.get("o")

    if args.get("db"):
        remaining_options["db"] = args.get("db")

    if args.get("dbq"):
        remaining_options["dbq"] = args.get("dbq")

    if args.get("s"):
        remaining_options["s"] = args.get("s")

    if args.get("knock"):
        remaining_options["knock"] = args.get("knock")

    if args.get("joke"):
        remaining_options["joke"] = args.get("joke")

    return remaining_options


def parse_user_scan_options(args):
    """Parse the user input and returns what scan options has been chosen.
    Default to connect scan when the scan type is omitted"""
    if args.get("tc"):
        return "tc"
    elif args.get("ts"):
        return "ts"
    elif args.get("tx"):
        return "tx"
    elif args.get("us"):
        return "us"
    else:
        print(f"{Fore.GREEN}--{Fore.RESET}No scan type has been specified defaulting to connect scan")
        return "tc"
