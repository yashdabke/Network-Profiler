#this edited code saves the WiFi details to a text file for future references
import subprocess
import socket
import speedtest
import csv

def get_wifi_profiles():
    try:
        # Use 'netsh' command to retrieve WiFi profiles
        data = (
            subprocess.check_output(["netsh", "wlan", "show", "profiles"])
            .decode("utf-8")
            .split("\n")
        )
        # Extract profile names
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        return profiles
    except subprocess.CalledProcessError:
        print("Error fetching WiFi profiles.")
        return []

def get_wifi_password(profile_name):
    try:
        # Use 'netsh' command to retrieve WiFi profile passwords
        results = (
            subprocess
            .check_output(["netsh", "wlan", "show", "profile", profile_name, "key=clear"])
            .decode("utf-8")
            .split("\n")
        )
        # Extract the password from the results
        password = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        if password:
            return password[0]
        else:
            return "No password found"
    except subprocess.CalledProcessError:
        return "Error fetching password"

def get_ip_address():
    try:
        # Get the hostname and resolve it to get the IP address
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error:
        return "Error fetching IP address"

def get_available_networks():
    try:
        # Use 'netsh' command to retrieve available WiFi networks
        networks = (
            subprocess.check_output(["netsh", "wlan", "show", "network"])
            .decode("utf-8")
            .split("\n")
        )
        # Extract SSID (network names)
        available_networks = [line.strip() for line in networks if "SSID" in line]
        return available_networks
    except subprocess.CalledProcessError:
        print("Error fetching available networks.")
        return []

def test_network_speed():
    try:
        # Use the 'speedtest' library to measure download and upload speeds
        st = speedtest.Speedtest()
        st.get_best_server()  # Find the best server for testing
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000  # Convert to Mbps
        return download_speed, upload_speed
    except Exception as e:
        return str(e)

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        # Write data to a text file
        for item in data:
            file.write(f"{item}\n")

def main():
    # Fetch WiFi profiles, IP address, available networks, and network speed
    wifi_profiles = get_wifi_profiles()
    ip_address = get_ip_address()
    available_networks = get_available_networks()
    download_speed, upload_speed = test_network_speed()

    # Save information to text files
    save_to_file(wifi_profiles, 'wifi_profiles.txt')
    save_to_file([ip_address], 'ip_address.txt')
    save_to_file(available_networks, 'available_networks.txt')
    save_to_file([f"Download Speed: {download_speed} Mbps", f"Upload Speed: {upload_speed} Mbps"], 'network_speed.txt')

    print("WiFi Profiles:")
    if wifi_profiles:
        for profile in wifi_profiles:
            password = get_wifi_password(profile)
            print("Profile: {:<30} | Password: {:<}".format(profile, password))
    else:
        print("No WiFi profiles found.")

    print("\nIP Address:")
    print(ip_address)

    print("\nAvailable Networks:")
    if available_networks:
        for network in available_networks:
            print(network)
    else:
        print("No available networks found.")

    print("\nNetwork Speed:")
    print(f"Download Speed: {download_speed} Mbps")
    print(f"Upload Speed: {upload_speed} Mbps")

if __name__ == "__main__":
    main()
