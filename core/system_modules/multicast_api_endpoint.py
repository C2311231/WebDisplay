"""
Multicast API Endpoint Module

Part of WebDisplay
System Multicast API Endpoint Module

License: MIT license

Author: C2311231

Notes:
- Manages multicast anouncments and state changes.
- Manages discovery
"""

import socket
import struct
import json
import time
import core.commons as commons
from core.system import system
import core.system_modules.database.settings_manager as settings_manager
import core.module
from core.system_modules.networking import NetworkingManager
from datetime import datetime
from core.system_modules.api.api_registry import APIRegistry

# TODO Reimplement Discovery Module
class DiscoveryEngine(core.module.module):
    def __init__(self, system: system):
        self.system = system
        system.require_modules("settings_manager", "networking_manager", "api_registery")
        self.api_send_id = 0
        
    def start(self) -> None:
        self.settings_manager: settings_manager.SettingsManager = self.system.get_module("settings_manager") # type: ignore
        self.networking: NetworkingManager = self.system.get_module("networing_module") # type: ignore
        self.api_registery: APIRegistry = self.system.get_module("api_registry") # type: ignore
        
        self.discovery_port = self.settings_manager.register_setting(domain="discovery", version="V1", setting_name="Discovery Port", default_value="5000", type="int", description="Port to be used for multicast discovery. (Must be the same across all devices)", validation_data={}, user_facing=True)
        self.discovery_multicast_address = self.settings_manager.register_setting(domain="discovery", version="V1", setting_name="Discovery Multicast Address", default_value="239.143.23.9", type="ip", description="Address to be used for multicast discovery. (Must be the same across all devices)", validation_data={"multicast": True}, user_facing=True)
    
    def send_discovery(self) -> None:
        """Send discovery message periodically."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2
        )  # Set TTL to 2 for local network

        while True:
            try:
                init_message = {
                "type": "discover",
                "id": self.settings_manager.get_setting("system", "id").get_value(),
                "ver": 1,
                "api": f"http://{self.networking.get_local_ip()}:{5000}/api",
                "caps": self.api_registery.get_capabilities(),
                "ts": str(datetime.now())
                }
                self.api_send_id += 1
                message = json.dumps(init_message, indent=4).encode()
                sock.sendto(
                    message, (str(self.discovery_multicast_address.get_value()), self.discovery_port.get_value())
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
        sock.bind(("", self.discovery_port.get_value()))

        group = socket.inet_aton(str(self.discovery_multicast_address.get_value()))
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
    
def register(system_manager):
    return "discovery_engine", DiscoveryEngine(system_manager)