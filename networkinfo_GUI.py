# pip install speedtest only for this code - provides a gui window to display network details 

import subprocess
import socket
import tkinter as tk
from tkinter import messagebox

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
        # Use 'speedtest-cli' as a command-line process to measure download speed
        speedtest_output = (
            subprocess.check_output(["speedtest-cli", "--simple"])
            .decode("utf-8")
            .split("\n")
        )

        # Extract download speed from the output
        for line in speedtest_output:
            if line.startswith("Download:"):
                download_speed = line.split()[1]
                return download_speed

        return "Speedtest failed"
    except subprocess.CalledProcessError:
        return "Error executing speedtest-cli"

def save_to_file(data, filename):
    with open(filename, 'w') as file:
        # Write data to a text file
        for item in data:
            file.write(f"{item}\n")

def fetch_data_and_save():
    # Fetch WiFi profiles, IP address, available networks, and network speed
    wifi_profiles = get_wifi_profiles()
    ip_address = get_ip_address()
    available_networks = get_available_networks()
    speed = test_network_speed()  # Get the network speed as a single value

    # Update labels with fetched information
    wifi_profiles_label.config(text="WiFi Profiles:\n" + "\n".join(wifi_profiles))
    ip_address_label.config(text="IP Address:\n" + ip_address)
    available_networks_label.config(text="Available Networks:\n" + "\n".join(available_networks))
    network_speed_label.config(text=f"Network Speed:\nDownload Speed: {speed} Mbps")

    # Save information to text files
    save_to_file(wifi_profiles, 'wifi_profiles.txt')
    save_to_file([ip_address], 'ip_address.txt')
    save_to_file(available_networks, 'available_networks.txt')
    save_to_file([f"Download Speed: {speed} Mbps"], 'network_speed.txt')

    messagebox.showinfo("Success", "Data has been fetched and saved successfully!")

def main():
    global wifi_profiles_label, ip_address_label, available_networks_label, network_speed_label

    window = tk.Tk()
    window.title("Network Info Tool")

    # Create a button to fetch data and save
    fetch_button = tk.Button(window, text="Fetch Data and Save", command=fetch_data_and_save)
    fetch_button.pack()

    # Create labels to display fetched information
    wifi_profiles_label = tk.Label(window, text="WiFi Profiles:")
    wifi_profiles_label.pack()

    ip_address_label = tk.Label(window, text="IP Address:")
    ip_address_label.pack()

    available_networks_label = tk.Label(window, text="Available Networks:")
    available_networks_label.pack()

    network_speed_label = tk.Label(window, text="Network Speed:")
    network_speed_label.pack()

    window.mainloop()

if __name__ == "__main__":
    main()
    
