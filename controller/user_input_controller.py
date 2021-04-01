import argparse

from model.user_input_model import check_ip, check_port, check_port_range, check_scan_options, check_user_input


def parse_user_arguments():
    """
    Parse command line input and derive variables
    needed to check for valid input by parsing
    the variables as arguments to other methods
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "-target", metavar="", type=str, required=True,
                        help="IP4V address that needs to be scanned")
    parser.add_argument("-p", "-port", metavar="", type=int, help="Single port e.g. 80")
    parser.add_argument("-pl", "-portlist", metavar="", nargs='+', type=int, help="Port list e.g. 21,22,80")
    parser.add_argument("-pr", "-portrange", metavar="", nargs='+', type=int, help="Port range e.g. 20-30")
    parser.add_argument("-to", "-timeout", metavar="", type=int, default=2, help="Timeout value (default 2)")
    parser.add_argument("-th", "-threading", metavar="", type=int, default=1, help="Amount of threads (default 1)")
    parser.add_argument("-o", "-output", metavar="", type=str, help="json or xml output format")
    parser.add_argument("-s", "-sound", metavar="", type=str, default=False,
                        help="Activates sound to inform when a scan has been finished")
    parser.add_argument("-tc", "-tcpconnect", metavar="", type=str, default=True,
                        help="tcp connect scan (default if scan type is omitted)")
    parser.add_argument("-ts", "-tcpsync", metavar="", type=str, default=False, help="tcp sync scan")
    parser.add_argument("-tx", "-tcpxmas", metavar="", type=str, default=False, help="tcp xmas scan")
    parser.add_argument("-us", "-udpscan", metavar="", type=str, default=False, help="udp scan")
    args = vars(parser.parse_args())

    ip = args.get("t")
    check_ip(ip)

    if args.get("p") is not None:
        check_port(args.get("p"))
    elif args.get("pl") is not None:
        check_port(args.get("pl"))
    elif args.get("pr") is not None:
        port_range = args.get("pr")
        if len(port_range) > 2:
            return print("Please specify a range with 2 integers e.g. -pr / -portrange 20 100")
        port_range = range(port_range[0], port_range[1])
        check_port_range(port_range)
    else:
        print("Something went wrong with the ports")

    scan_type_tc = args.get("tc")
    scan_type_ts = args.get("ts")
    scan_type_tx = args.get("tx")
    scan_type_us = args.get("us")
    check_scan_options(scan_type_tc)
    # print(args)

    # check_user_input(ip, port, port_list,  port_range, scan_type_tc,
    #                  scan_type_ts, scan_type_tx, scan_type_us)

# class UserInput:
#
#     # def __init__(self):
#     #     self.success = success
#
#     def get_user_input(self, ip: IPv4Address, port: [MIN_PORT_NUMBER, 1000],
#                        scan_options: [], success: bool):
#         """collect the user input and parse it to the model layer"""
#
#         self.check_ip(ip)
#         self.check_port(port)
#         self.check_scan_options(scan_options)
