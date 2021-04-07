from datetime import datetime
import colorama
from colorama import Fore
import pyttsx3

colorama.init()


def start_scan_info(ip, scan_type):
    """Print starting header about the scan that is being run"""

    tick = datetime.now()
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print(f"Scan type: {scan_type}")
    print(f"Scanning target: {ip}")
    print(f"Scan started at: {tick}")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print("")

    return tick


def finish_scan_info(port_counter, tick, scan_data_object):
    """Print closing footer about the scan that is being run"""
    ports = scan_data_object.ports
    write_output_to_file = scan_data_object.output_to_file
    save_output_in_database = scan_data_object.save_to_database
    sound = scan_data_object.sound

    tock = datetime.now()
    scan_time = tock - tick

    print("")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print(f"total of {port_counter} port(s) open out of the {len(ports)} port(s) scanned")
    print(f"Scan completed in: {scan_time}")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")

    if write_output_to_file:
        print(f"{Fore.GREEN}--{Fore.RESET} output saved to JSON and XML within the \"scan_output\" folder")
    if save_output_in_database:
        print(f"{Fore.GREEN}--{Fore.RESET} output saved to database: \"scan_result.db\" within the repository folder")
    if sound:
        alert_scan_finish_with_sound(sound)


def alert_scan_finish_with_sound(sound_on):
    """Turn on sound to notify the user the scan has finished"""
    engine = pyttsx3.init()
    engine.setProperty('rate', 120)  # voice speed
    # todo male voice
    engine.say("Port scanner is finished")
    engine.runAndWait()
    engine.stop()

