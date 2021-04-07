from sys import platform
from datetime import datetime
import json, xml, os


def save_scan_info_to_file(ip, port, banner, scan_type):
    """parse scan data into json and xml file methods"""
    directory = check_platform()

    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y_time_%H-%M")

    json_format(ip, port, banner, scan_type, date_time, directory)

    xml_format(ip, port, banner, scan_type, date_time, directory)


def json_format(ip, port, banner, scan_type, date_time, directory):
    """parse scan data into json format"""
    json_file = f'IP_{ip}_DATE_{date_time}.json'
    json_file = os.path.join(directory, json_file)

    with open(json_file, 'w') as file:
        pass


def xml_format(ip, port, banner, scan_type, date_time, directory):
    """parse scan data into xml format"""
    xml_file = f'IP_{ip}_DATE_{date_time}.xml'
    xml_file = os.path.join(directory, xml_file)

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
