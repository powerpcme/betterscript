import os
import netifaces as ni
import random

def get_interfaces():
    """
    Get a list of available network interfaces.
    """
    interfaces = ni.interfaces()
    return interfaces

def random_mac():
    """
    Generate a random MAC address.
    """
    mac = [ 0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)
          ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

print("Welcome to the Bettercap automation script!")
print("Please select a network interface to use:")
interfaces = get_interfaces()
for i, interface in enumerate(interfaces):
    print(f"{i+1}. {interface}")
option = input("Enter your choice: ")

try:
    iface = interfaces[int(option)-1]
except IndexError:
    print("Invalid option. Please try again.")
    exit()

print(f"Using {iface} interface")

print("Please select an option from the following menu:")
print("1. Scan for devices")
print("2. Spoof MAC address")
print("3. Intercept and modify traffic")
print("4. Exit")

option = input("Enter your choice: ")

if option == "1":
    print("Scanning for devices...")
    os.system(f"sudo bettercap -iface {iface} -sniff")
elif option == "2":
    print("Please select an option for MAC address:")
    print("1. Input MAC address manually")
    print("2. Generate random MAC address")
    mac_option = input("Enter your choice: ")
    if mac_option == "1":
        new_mac = input("Enter the new MAC address: ")
    elif mac_option == "2":
        new_mac = random_mac()
        print(f"Generated random MAC address: {new_mac}")
    else:
        print("Invalid option. Please try again.")
        exit()
    print(f"Spoofing MAC address to {new_mac}...")
    os.system(f"sudo ifconfig {iface} down")
    os.system(f"sudo ifconfig {iface} hw ether {new_mac}")
    os.system(f"sudo ifconfig {iface} up")
elif option == "3":
    print("Intercepting and modifying traffic...")
    os.system(f"sudo bettercap -iface {iface} -proxy -tcp-proxy -caplet http.cap")
elif option == "4":
    print("Exiting...")
else:
    print("Invalid option. Please try again.")
