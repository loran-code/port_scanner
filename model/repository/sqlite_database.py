import os
import sqlite3
import socket
from datetime import datetime
from sqlite3 import DatabaseError

directory = "model\\repository\\"
parent_directory = os.getcwd()
print(parent_directory)
path = os.path.join(parent_directory, directory)
connection = sqlite3.connect(rf'{path}scan_results.db')  # Opens Connection to SQLite database
cursor = connection.cursor()


def save_scan_info_to_database(scan_output):
    """bla bla"""
    print(path)
    print(parent_directory)
    create_db()  # Creates database table
    data_entry(scan_output)  # Parse the scan output into the database table
    print("created db object")


def create_db():
    """Creates a table within the database file if it does not exists"""
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS scan_results (id integer PRIMARY KEY,"
                       "date_time timestamp,"
                       "ip TEXT, scan_type TEXT, "
                       "open_ports TEXT, banner TEXT, scanned_by_computer TEXT)")
    except DatabaseError:
        print(DatabaseError)


def data_entry(scan_output):
    """Inserts data into table and close the connection"""
    now = datetime.now()
    date_time = now.strftime("%d-%m-%Y %H:%M:%S")
    computer_name = socket.gethostname()

    # Get scan output values from dictionary
    ip = scan_output.get("ip")
    scan_type = scan_output.get("scan type")

    open_ports = scan_output['open ports'][0]['port']
    print(open_ports)
    open_ports = 1
    # for i in range(len(open_ports)):
    #     print(i)
    banner = scan_output['open ports'][0]['banner']
    banner = 2
    # print(banner)
    # for i in range(len(banner)):
    #     print(i)

    # Insert values into the db table
    params = (date_time, ip, scan_type, open_ports, banner, computer_name)
    cursor.execute("INSERT INTO scan_results (date_time, ip, scan_type, open_ports, banner, computer_name)"
                   " VALUES (?,?,?,?,?,?)", params)

    connection.commit()

    cursor.close()
    connection.close()
