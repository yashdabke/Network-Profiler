# Import necessary modules
import pathlib
import sys
import argparse
from shutil import which
import re
import os

# Import custom utility functions and constants
import utils
import constants

# Define the script's version
__version__ = "1.1.1"

# Function to print an error message and exit the program with an error status
def print_error(text) -> None:
    print(f"ERROR: {text}", file=sys.stderr)
    sys.exit(1)

# Function to get the SSID of the currently connected Wi-Fi network
def get_ssid() -> str:
    # Determine the platform (e.g., macOS, Linux, Windows)
    platform = utils.get_platform()

    if platform == constants.MAC:
        # On macOS, use the 'airport' command to obtain SSID information
        airport = pathlib.Path(constants.AIRPORT_PATH)

        if not airport.is_file():
            # Check if the 'airport' command is available
            print_error(f"Can't find 'airport' command at {airport}")

        # Run the 'airport' command and extract the SSID
        ssid = utils.run_command(f"{airport} -I | awk '/ SSID/ {{print substr($0, index($0, $2))}}'")

    elif platform == constants.LINUX:
        # On Linux, use 'nmcli' to obtain SSID information
        if which("nmcli") is None:
            # Check if Network Manager is available
            print_error("Network Manager is required to run this program on Linux.")

        # Run 'nmcli' to get SSID information
        ssid = utils.run_command("nmcli -t -f active,ssid dev wifi | egrep '^yes:' | sed 's/^yes://'")

    elif platform == constants.WINDOWS:
        # On Windows, use 'netsh' to obtain SSID information
        ssid = utils.run_command("netsh wlan show interfaces | findstr SSID")

        if ssid == "":
            # Check if SSID was found
            print_error("SSID was not found")

        # Extract the SSID from the output
        ssid = re.findall(r"[^B]SSID\s+:\s(.*)", ssid)[0]

    return ssid

# Main function to handle command-line arguments and perform actions
def main() -> None:
    # Create an argument parser
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")

    # Define command-line options and their descriptions
    parser.add_argument("--show-qr", "-show",
                        action="store_true",
                        default=False,
                        help="Show an ASCII QR code on the terminal/console")

    parser.add_argument("--save-qr", "-save",
                        metavar="PATH",
                        nargs="?",
                        const="STORE_LOCALLY",
                        help="Create a QR code and save it as an image")

    parser.add_argument("--ssid", "-s",
                        help="Specify an SSID that you have previously connected to")

    parser.add_argument('--list', "-l", 
                        action="store_true", 
                        default=False, 
                        help="List all stored network SSID")

    parser.add_argument("--version",
                        action="store_true",
                        help="Show the script's version number")
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # If the --version option is provided, print the version and exit
    if args.version:
        print(__version__)
        sys.exit()

    # Initialize a dictionary to store Wi-Fi SSID information
    wifi_dict = {}

    # If the --list option is provided, list stored network SSIDs
    if args.list:
        # Get a list of Wi-Fi profiles and generate a dictionary
        profiles = utils.get_profiles()
        wifi_dict = utils.generate_wifi_dict(profiles)
        utils.print_dict(wifi_dict)
        return

    # If no SSID is specified, use the SSID of the currently connected network
    if args.ssid is None:
        args.ssid = get_ssid()

    # Split SSIDs if multiple SSIDs are provided
    ssid = get_ssid() if not args.ssid else args.ssid.split(',')

    # Generate a dictionary of SSIDs and their associated information
    if ssid:
        wifi_dict = utils.generate_wifi_dict(ssid)

    # If the --show-qr or --save-qr option is provided, generate QR codes
    if args.show_qr or args.save_qr:
        for key, value in wifi_dict.items():
            utils.generate_qr_code(ssid=key, password=value, path=args.save_qr, show_qr=args.show_qr)
        return

    # If none of the above options are provided, print the Wi-Fi SSID information
    utils.print_dict(wifi_dict)

# Check if the script is run as the main program
if __name__ == "__main__":
    main()
