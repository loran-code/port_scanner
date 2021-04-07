from sys import platform
from datetime import datetime
import json, xml, os


def save_scan_info_to_file(scan_output):
    """parse scan data into json and xml file methods"""
    directory = check_platform()

    # json_format(scan_output, directory)

    xml_format(scan_output, directory)


def json_format(scan_output, directory):
    """parse scan data into json format"""
    ip = scan_output.get("ip")
    date_time = scan_output.get("date time")

    json_file = f'IP_{ip}_DATE_{date_time}.json'
    json_file = os.path.join(directory, json_file)

    with open(json_file, 'w') as file:
        # json.dump(scan_output)
        file.write(json.dumps(scan_output, indent=1))


def xml_format(scan_output, directory):
    """parse scan data into xml format"""
    ip = scan_output.get("ip")
    date_time = scan_output.get("date time")

    xml_file = f'IP_{ip}_DATE_{date_time}.xml'
    xml_file = os.path.join(directory, xml_file)

    # xml.parsers
    with open(xml_file, 'w') as file:
        pass


def check_platform():
    """Check what the underlying os is and create a directory
    where the output of the scan is being saved"""
    directory = "scan_output"
    mode = 0o666

    if platform == "linux" or platform == "linux2":  # linux
        parent_directory = os.getcwd()
        path = os.path.join(parent_directory, directory)

        if os.path.exists(path):
            return path

        try:
            os.mkdir(path, mode)
            return path
        except OSError as error:
            print(error)

    if platform == "darwin":  # OS X
        parent_directory = os.getcwd()
        path = os.path.join(parent_directory, directory)

        if os.path.exists(path):
            return path

        try:
            os.mkdir(path, mode)
            return path
        except OSError as error:
            print(error)

    if platform == "win32":  # Windows
        parent_directory = os.getcwd()
        path = os.path.join(parent_directory, directory)

        if os.path.exists(path):
            return path

        try:
            os.mkdir(path, mode)
            return path
        except OSError as error:
            print(error)
