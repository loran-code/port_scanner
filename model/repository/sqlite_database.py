import os
import sqlite3
import socket
from sqlite3 import DatabaseError

#  Database setup requirements
directory = "model\\repository\\"
parent_directory = os.getcwd()
path = os.path.join(parent_directory, directory)
connection = sqlite3.connect(rf'{path}scan_results.db')  # Opens Connection to SQLite database
cursor = connection.cursor()


def save_scan_info_to_database(scan_output):
    """Database connection setup"""
    create_db()  # Creates database table
    data_entry(scan_output)  # Parse the scan output into the database table


def create_db():
    """Creates a table within the database file if it does not exists"""
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS scan_results (id INTEGER PRIMARY KEY,"
                       "date_time timestamp,"
                       "ip TEXT, scan_type TEXT, scanned_ports TEXT,"
                       "open_ports TEXT, open_or_filtered_ports TEXT,"
                       " filtered_ports TEXT, banner TEXT, scanned_by_computer TEXT)")
    except DatabaseError:
        print(DatabaseError)


def data_entry(scan_output):
    """Inserts data into database table and close the connection"""
    computer_name = socket.gethostname()

    # Get scan output values from dictionary
    date_time = scan_output.get("date time")
    ip = scan_output.get("ip")
    scan_type = scan_output.get("scan type")

    scanned_ports = scan_output.get("scanned ports")
    all_ports = parse_scannend_ports(scanned_ports)

    ports = scan_output['open ports']['port number']
    open_ports = parse_scannend_open_ports(ports)

    open_banners = ""
    try:  # Checks if tcp connect (banner grab) scan has been used

        if scan_output['open ports']['banner'] is not None:
            banners = scan_output['open ports']['banner']
            open_banners = parse_scanned_banners(banners)

    except KeyError:  # tcp connect has not been used
        pass

    open_or_filtered_port_list = ""
    try:  # Checks if scan has found open or filtered ports
        if scan_output['open or filtered ports']['port number'] is not None:
            open_or_filtered_ports = scan_output['open or filtered ports']['port number']
            open_or_filtered_port_list = parse_scanned_open_or_filtered_ports(open_or_filtered_ports)

    except KeyError:  # Open or filtered ports have not been found
        pass

    filtered_port_list = ""
    try:  # Checks if scan has found filtered ports

        if scan_output['filtered ports']['port number'] is not None:
            filtered_ports = scan_output['filtered ports']['port number']
            filtered_port_list = parse_scanned_filtered_ports(filtered_ports)

    except KeyError:  # Filtered ports have not been found
        pass

    # all_ports = ""  # Uncomment code if you do not want to insert all the scannend ports into the database.

    # Insert values into the db table
    params = (date_time, ip, scan_type, all_ports, open_ports, open_or_filtered_port_list,
              filtered_port_list, open_banners, computer_name)

    cursor.execute("INSERT INTO scan_results (date_time, ip, scan_type, scanned_ports,"
                   " open_ports, open_or_filtered_ports, filtered_ports, banner, scanned_by_computer) "
                   " VALUES (?,?,?,?,?,?,?,?,?)", params)

    connection.commit()  # Commit the selected data into the database

    cursor.close()
    connection.close()


def query_db(ip):
    """Query the database and return all the info on the specified ip address"""
    try:
        cursor.execute("SELECT * FROM scan_results WHERE ip=?", (ip,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            print(f"There is no stored data on IP: {ip}")
        else:
            for row in rows:
                print(row)

    except DatabaseError:
        print(DatabaseError)

    cursor.close()
    connection.close()


def parse_scannend_ports(scanned_ports):
    """parse the values of a list into a string"""
    all_ports = ""

    for port in scanned_ports:
        port = str(port)
        all_ports += f"{port}, "

    all_ports = all_ports[:-2]

    return all_ports


def parse_scannend_open_ports(ports):
    """parse the values of a list into a string"""
    open_ports = ""

    for port in ports:
        port = str(port)
        open_ports += f"{port}, "

    open_ports = open_ports[:-2]

    return open_ports


def parse_scanned_banners(banners):
    """parse the values of a list into a string"""
    open_banners = ""

    for banner in banners:
        open_banners += f"{banner}, "
    open_banners = open_banners[:-2]

    return open_banners


def parse_scanned_open_or_filtered_ports(open_or_filtered_ports):
    """parse the values of a list into a string"""
    open_or_filtered_port_list = ""

    for port in open_or_filtered_ports:
        port = str(port)
        open_or_filtered_port_list += f"{port}, "

    open_or_filtered_port_list = open_or_filtered_port_list[:-2]

    return open_or_filtered_port_list


def parse_scanned_filtered_ports(filtered_ports):
    """parse the values of a list into a string"""
    filtered_port_list = ""

    for port in filtered_ports:
        port = str(port)
        filtered_port_list += f"{port}, "

    filtered_port_list = filtered_port_list[:-2]

    return filtered_port_list
