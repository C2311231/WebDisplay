import os
import subprocess
from base import commons
import socket
class NetworkingManager(commons.BaseClass):
    def __init__(self, database):
        self.database = database

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

    def configure_static(self, ip: commons.address, gateway: commons.address, dns: commons.address, interface: str) -> None:
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

    def tick(self) -> None:
        # Run any maintenance tasks and checks (about every 5 seconds)
        pass

    def required_config(self) -> dict:
        # Required configuration data in database in format {parameter: default} (None results in defaulting to parameters set by other classes, if none are set an error will be thrown)
        data = {
            "web_version": None,
            "api_version": None,
            "web_url": None,
            "web_port": None,
            "web_encryption": None,
            "device_name": None,
            "device_state": None,
            "device_platform": None,
            "device_id": None,
            "device_ip": None,
        }
        return data

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

    # if __name__ == "__main__":
    #     # Start both send and listen threads
    #     threading.Thread(target=send_discovery, daemon=True).start()
    #     threading.Thread(target=listen_for_discovery, daemon=True).start()

    #     # Keep the main thread alive
    #     while True:
    #         time.sleep(1)