"""
Networking Module Manager

Part of WebDisplay
System Networking Module

License: MIT license

Author: C2311231

Notes:
"""

import os
import subprocess
import core.module
import socket
import core.commons as commons
import core.system as system
import core.system_modules.database.settings_manager as settings_manager

class NetworkingManager(core.module.module):
    def __init__(self, system: system.system):
        self.system = system
        system.require_modules("settings_manager")
        
    def start(self) -> None:
        self.settings_manager: settings_manager.SettingsManager = self.system.get_module("settings_manager") # type: ignore

    def configure_wifi(self, ssid: str, psk: str) -> None:
        command = f'nmcli dev wifi connect "{ssid}" password "{psk}"'
        result = os.system(command)
        if result == 0:
            print(f"Successfully connected to SSID: {ssid}")
        else:
            print(
                f"Failed to connect to SSID: {ssid}. Check your credentials or WiFi availability."
            )

    def configure_dhcp(self, interface: str) -> None:
        command = f"nmcli con mod {interface} ipv4.method auto"
        os.system(command)
        os.system(f"nmcli con up {interface}")
        print(f"Ethernet ({interface}) configured to use DHCP.")

    def configure_static(self, ip: commons.Address, gateway: commons.Address, dns: commons.Address, interface: str) -> None:
        os.system(f"nmcli con mod {interface} ipv4.addresses {ip}/24")
        os.system(f"nmcli con mod {interface} ipv4.gateway {gateway}")
        os.system(f"nmcli con mod {interface} ipv4.dns {dns}")
        os.system(f"nmcli con mod {interface} ipv4.method manual")
        os.system(f"nmcli con up {interface}")
        print(f"Ethernet ({interface}) configured with static IP: {ip}")

    def get_interfaces(self) -> list[dict]:
        # result = subprocess.run(["nmcli", "device", "status"], stdout=subprocess.PIPE, text=True)
        # lines = result.stdout.splitlines()[1:]  # Skip the first line (header)

        # interfaces = []
        # for line in lines:
        #     parts = line.split()
        #     interface = {
        #         "name": parts[0],
        #         "type": parts[1],
        #         "state": parts[2],
        #         "data": get_interface_details(parts[0])
        #     }
        #     interfaces.append(interface)
        interfaces = [
            {
                "name": "eth0",
                "type": "Ethernet",
                "state": "online",
                "data": {
                    "ip_address": "987.123.123.321",
                    "dns": "1.1.1.1",
                    "gateway": "987.123.123.1",
                },
            },
            {
                "name": "eth1",
                "type": "Ethernet",
                "state": "online",
                "data": {
                    "ip_address": "987.123.123.321",
                    "dns": "1.1.1.1",
                    "gateway": "987.123.123.1",
                },
            },
            {
                "name": "wlps1",
                "type": "WiFi",
                "state": "online",
                "data": {
                    "ip_address": "987.123.123.321",
                    "dns": "1.1.1.1",
                    "gateway": "987.123.123.1",
                },
            },
        ]
        return interfaces

    def get_interface_details(self, interface) -> dict:
        result = subprocess.run(
            ["nmcli", "device", "show", interface], stdout=subprocess.PIPE, text=True
        )
        details = result.stdout.splitlines()

        info = {}
        for line in details:
            if "IP4.ADDRESS" in line:
                info["ip_address"] = line.split(":")[1].strip()
            elif "IP4.GATEWAY" in line:
                info["gateway"] = line.split(":")[1].strip()
            elif "IP4.DNS" in line:
                if "dns" not in info:
                    info["dns"] = []
                info["dns"].append(line.split(":")[1].strip())
            elif "GENERAL.HWADDR" in line:
                info["mac_address"] = line.split(":", 1)[1].strip()

        return info

    def update(self, delta_time: float) -> None:
        pass

    def get_local_ip(self):
        try:
            # Connect to an external server (Google's DNS) to determine the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "Unable to determine local IP"
        
def register(system_manager):
    return "networking", NetworkingManager(system_manager)