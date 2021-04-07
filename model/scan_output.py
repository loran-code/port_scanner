import json
import os
from datetime import datetime
from sys import platform
import xml.etree.ElementTree as ET


def save_scan_info_to_file(scan_output):
    """parse scan data into json and xml file methods"""
    directory = check_platform()

    json_format(scan_output, directory)  # JSON file

    xml_format(scan_output, directory)  # XML file


def json_format(scan_output, directory):
    """parse scan data into json format"""
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y_time_%H-%M")
    ip = scan_output.get("ip")

    json_file = f'IP_{ip}_DATE_{date_time}.json'
    json_file = os.path.join(directory, json_file)

    with open(json_file, 'w') as file:
        file.write(json.dumps(scan_output, indent=1))


def xml_format(scan_output, directory):
    """parse scan data into xml format"""
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y_time_%H-%M")
    ip = scan_output.get("ip")

    xml_file = f'IP_{ip}_DATE_{date_time}.xml'
    xml_file = os.path.join(directory, xml_file)

    root = ET.Element('scan_results')

    date_time = ET.SubElement(root, 'date')
    date_time.text = scan_output.get("date time")

    ip = ET.SubElement(root, 'host')
    ip.text = scan_output.get("ip")

    scan_type = ET.SubElement(root, 'type')
    scan_type.text = scan_output.get("scan type")

    ports = ET.SubElement(root, 'ports')

    for port in scan_output.get("scanned ports"):
        scannend_ports = ET.SubElement(ports, 'scannedports')
        scannend_ports.text = str(port)

    open_ports = ET.SubElement(ports, 'openports')
    for port in scan_output['open ports'][0]['port']:
        open_ports.text = str(port)

    banner = ET.SubElement(open_ports, 'banner')
    for i in scan_output['open ports'][0]['banner']:
        banner.text = str(i)

    # todo bytes vs string & spread output instead of 1 line
    data_to_xml = ET.tostringlist(root)

    with open(xml_file, 'w') as file:
        file.write(str(data_to_xml))


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
