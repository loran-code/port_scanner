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


def finish_scan_info(port_counter, ports, tick, sound_on):
    """Print closing footer about the scan that is being run"""
    tock = datetime.now()
    scan_time = tock - tick
    print("")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print(f"total of {port_counter} port(s) open out of the {len(ports)} port(s) scanned")
    print(f"Scan completed in: {scan_time}")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    alert_scan_finish_with_sound(sound_on)


def alert_scan_finish_with_sound(sound_on):
    """Turn on sound to notify the user the scan has finished"""

    if sound_on:
        engine = pyttsx3.init()
        engine.setProperty('rate', 120)  # voice speed
        engine.setProperty('volume', 1)  # Volume
        # todo male voice
        engine.say("Port scanner is finished")
        engine.runAndWait()
        engine.stop()
    else:
        return None
