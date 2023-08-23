import subprocess
import socket

def get_wifi_profiles():
    try:
        data = (
            subprocess.check_output(["netsh", "wlan", "show", "profiles"])
            .decode("utf-8")
            .split("\n")
        )
        profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]
        return profiles
    except subprocess.CalledProcessError:
        print("Error fetching WiFi profiles.")
        return []

def get_wifi_password(profile_name):
    try:
        results = (
            subprocess
            .check_output(["netsh", "wlan", "show", "profile", profile_name, "key=clear"])
            .decode("utf-8")
            .split("\n")
        )
        password = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        if password:
            return password[0]
        else:
            return "No password found"
    except subprocess.CalledProcessError:
        return "Error fetching password"

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error:
        return "Error fetching IP address"

def get_available_networks():
    try:
        networks = (
            subprocess.check_output(["netsh", "wlan", "show", "network"])
            .decode("utf-8")
            .split("\n")
        )
        available_networks = [line.strip() for line in networks if "SSID" in line]
        return available_networks
    except subprocess.CalledProcessError:
        print("Error fetching available networks.")
        return []

def main():
    wifi_profiles = get_wifi_profiles()
    ip_address = get_ip_address()
    available_networks = get_available_networks()

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

if __name__ == "__main__":
    main()
