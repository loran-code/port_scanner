import os
import sqlite3
import socket
from datetime import datetime
from sqlite3 import DatabaseError

directory = "model\\repository\\"
parent_directory = os.getcwd()
path = os.path.join(parent_directory, directory)
# async with sqlite3.connect(rf'{path}scan_results.db') as connection:
connection = sqlite3.connect(rf'{path}scan_results.db')  # Opens Connection to SQLite database
cursor = connection.cursor()


async def save_scan_info_to_database(scan_output):
    """Database connection setup"""

    create_db()  # Creates database table
    data_entry(scan_output)  # Parse the scan output into the database table


def create_db():
    """Creates a table within the database file if it does not exists"""

    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS scan_results (id INTEGER PRIMARY KEY,"
                       "date_time timestamp,"
                       "ip TEXT, scan_type TEXT, scanned_ports TEXT,"
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
    scanned_ports = scan_output.get("scanned ports")
    ports = scan_output['open ports']['number']
    banners = scan_output['open ports']['banner']

    all_ports = ""
    for port in scanned_ports:
        port = str(port)
        all_ports += f"{port}, "

    open_ports = ""
    for port in ports:
        port = str(port)
        open_ports += f"{port}, "

    open_banners = ""
    for banner in banners:
        open_banners += f"{banner}, "

    # Insert values into the db table
    params = (date_time, ip, scan_type, all_ports, open_ports, open_banners, computer_name)

    cursor.execute("INSERT INTO scan_results (date_time, ip, scan_type, scanned_ports,"
                   " open_ports, banner, scanned_by_computer) "
                   " VALUES (?,?,?,?,?,?,?)", params)

    connection.commit()

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
