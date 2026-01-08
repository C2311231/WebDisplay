import socket
import struct
import json
import time
import core.commons as commons
from core.system import system
import core.system_modules.database.settings_manager as settings_manager
import core.module
class DiscoveryEngine(core.module.module):
    def __init__(self, system: system):
        self.system = system
        system.require_modules("settings_manager")
        self.discovery_port = 5000 #TODO load this from config
        self.discovery_multicast_address = commons.Address("239.143.23.9") #TODO load this from config
        self.api_send_id = 0
        
    def start(self) -> None:
        self.settings_manager: settings_manager.SettingsManager = self.system.get_module("settings_manager") # type: ignore

    
    def send_discovery(self) -> None:
        """Send discovery message periodically."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2
        )  # Set TTL to 2 for local network

        while True:
            try:
                init_message = {
                    "id": self.api_send_id,
                    "type": "inform",
                    "version": "v2",
                    "destination": "0",  # 0 means all devices
                    "source": self.settings_manager.get_setting("device_id").get_value(),
                    "domain": "peer_manager",
                    "name": "discovery",
                    "data": {
                        "device_name": self.settings_manager.get_setting("device_name").get_value(),
                        "device_id": self.settings_manager.get_setting("device_id").get_value(),
                        "device_ip": self.settings_manager.get_setting("device_ip").get_value(),
                        "device_port": self.settings_manager.get_setting("device_port").get_value(),
                    }
                }
                self.api_send_id += 1
                message = json.dumps(init_message, indent=4).encode()
                sock.sendto(
                    message, (str(self.discovery_multicast_address), self.discovery_port)
                )
            except Exception as e:
                print(f"An error ocured when trying to send an auto discovery message: {e}")
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
                    sock.setsockopt(
                        socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2
                    )  # Set TTL to 2 for local network
                except:
                    print("Failed to reinitialize")
            time.sleep(5)  # Send every 5 seconds

    def listen_for_api_commands(self) -> None:
        """Listen for discovery messages."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", self.discovery_port))

        group = socket.inet_aton(str(self.discovery_multicast_address))
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        while True:
            data, address = sock.recvfrom(2048)

            try:
                data = json.loads(data.decode())
                
            except ValueError:
                print(f"Invalid Message from {address}")

    def update(self, delta_time: float) -> None:
        pass

    def register_required_config(self) -> None:
        # TODO source ip data from networking module
        self.settings_manager.register_required_settings("web_version", "api_version", "web_url", "web_port", "web_encryption", "device_name", 
                                                         "device_state", "device_platform", "device_id", "device_ip")
    
    
def register(system_manager):
    return "discovery_engine", DiscoveryEngine(system_manager)