#pip install speedtest-cli : This library allows you to measure the download, upload, and ping speeds of the current network connection

import subprocess
import socket
import speedtest

# Function to get WiFi profiles stored on the system
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

# Function to get the WiFi password for a given profile
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

# Function to get the IP address of the local machine
def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error:
        return "Error fetching IP address"

# Function to get available WiFi networks
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

# Function to perform a speed test and get download and upload speeds
def perform_speed_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()  # Find the best server for accurate results
        download_speed = st.download() / 10**6  # Convert to Mbps
        upload_speed = st.upload() / 10**6  # Convert to Mbps
        return download_speed, upload_speed
    except speedtest.SpeedtestException:
        return None, None

# Main function
def main():
    wifi_profiles = get_wifi_profiles()
    ip_address = get_ip_address()
    available_networks = get_available_networks()
    download_speed, upload_speed = perform_speed_test()

    # Display WiFi profiles
    print("WiFi Profiles:")
    if wifi_profiles:
        for profile in wifi_profiles:
            password = get_wifi_password(profile)
            print("Profile: {:<30} | Password: {:<}".format(profile, password))
    else:
        print("No WiFi profiles found.")

    # Display IP address
    print("\nIP Address:")
    print(ip_address)

    # Display available networks
    print("\nAvailable Networks:")
    if available_networks:
        for network in available_networks:
            print(network)
    else:
        print("No available networks found.")

    # Display speed test results
    print("\nSpeed Test:")
    if download_speed is not None and upload_speed is not None:
        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
    else:
        print("Speed test failed.")

if __name__ == "__main__":
    main()
