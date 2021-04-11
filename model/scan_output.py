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
    scan_output.pop("scanned ports")  # Comment out the code if you want to list all the scanned ports

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

    # Uncomment below code block if you want to list all the scanned ports.
    # for port in scan_output.get("scanned ports"):
    #     scannend_ports = ET.SubElement(ports, 'scannedports')
    #     scannend_ports.text = str(port)

    open_ports = scan_output['open ports']['port number']

    try:  # Checks if tcp connect (banner grab) scan has been used

        if scan_output['open ports']['banner'] is not None:
            banners = scan_output['open ports']['banner']

            ports_banners = zip(open_ports, banners)

            for port, banner in ports_banners:
                open_port = ET.SubElement(ports, 'open')
                open_port.text = str(port)
                open_banner = ET.SubElement(open_port, 'banner')
                open_banner.text = str(banner)

    except KeyError:  # tcp connect has not been used
        pass

    try:  # Checks if scan has found filtered ports
        filtered_ports = scan_output['filtered ports']['port number']

        for port in filtered_ports:
            filtered_port = ET.SubElement(ports, 'filtered')
            filtered_port.text = str(port)

        for port in open_ports:
            open_port = ET.SubElement(ports, 'open')
            open_port.text = str(port)

    except KeyError:  # Filtered ports have not been found
        pass

    data_to_xml = ET.tostring(root, encoding='unicode', method='xml')

    with open(xml_file, 'w') as file:
        file.write(data_to_xml)


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
