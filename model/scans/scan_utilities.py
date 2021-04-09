import asyncio
from datetime import datetime
import colorama
from colorama import Fore
import pyttsx3

colorama.init()


def start_scan_info(ip, scan_type):
    """Print starting header information about the scan that is being run"""

    tick = datetime.now()
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print(f"Scan type: {scan_type}")
    print(f"Scanning target: {ip}")
    print(f"Scan started at: {tick}")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")

    return tick


def finish_scan_info(port_counter, tick, scan_data_object):
    """Print closing footer information about the scan that is being run"""

    ports = scan_data_object.ports
    write_output_to_file = scan_data_object.output_to_file
    save_output_in_database = scan_data_object.save_to_database
    sound = scan_data_object.sound

    tock = datetime.now()
    scan_time = tock - tick

    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")
    print(f"total of {port_counter} port(s) are {Fore.GREEN}open{Fore.RESET} / {Fore.YELLOW}filtered{Fore.RESET}"
          f" out of the {len(ports)} port(s) scanned")
    print(f"Scan completed in: {scan_time}")
    print(60 * f"{Fore.YELLOW}-{Fore.RESET}")

    if write_output_to_file:
        print(f"{Fore.GREEN}--{Fore.RESET} output saved to JSON and XML within the \"scan_output\" folder")
    if save_output_in_database:
        print(f"{Fore.GREEN}--{Fore.RESET} output saved to database: \"scan_result.db\" within the repository folder")
    if sound:
        alert_scan_finish_with_sound()


def alert_scan_finish_with_sound():
    """Turn on sound to notify the user the scan has finished"""

    engine = pyttsx3.init()
    engine.setProperty('rate', 120)  # voice speed
    engine.say("Port scanner is finished")
    engine.runAndWait()
    engine.stop()


async def play_knocking_sound():
    """"Turn on a knocking sound in order to enhance the port scanning experience"""

    await asyncio.sleep(0)

    import playsound
    directory = "view/static/sound"
    playsound.playsound(f"{directory}/knock.mp3", True)
    await asyncio.sleep(1)


async def play_joke():
    """"Play a knocking joke, I bet people will love this!"""

    await asyncio.sleep(0)

    engine = pyttsx3.init()
    engine.setProperty('rate', 120)  # voice speed
    engine.say("Knock Knock")
    engine.say("Who is there?")
    engine.say("UDP")
    engine.say("UDP who?")
    engine.runAndWait()
    engine.stop()

# asyncio.gather(play_knocking_sound())
# asyncio.gather(play_joke())
# asyncio.get_event_loop().is_running()
