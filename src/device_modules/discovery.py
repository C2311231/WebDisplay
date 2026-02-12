"""
Multicast Discovery Module

Part of WebDisplay
device Discovery Module

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
from src.device import Device
import src.device_modules.database.settings_manager as settings_manager
import src.module
from src.device_modules.networking import NetworkingManager
from datetime import datetime
from src.device_modules.api import APIRegistry

class DiscoveryEngine(src.module.module):
    def __init__(self, device: Device):
        self.device = device
        device.require_modules("settings_manager", "networking", "api_registry")
        self.api_send_id = 0
        self.last_send_time = time.time()
        self.remotes = {}
        
    def start(self) -> None:
        self.settings_manager: settings_manager.SettingsManager = self.device.get_module("settings_manager") # type: ignore
        self.networking: NetworkingManager = self.device.get_module("networking") # type: ignore
        self.api_registery: APIRegistry = self.device.get_module("api_registry") # type: ignore
        self.device_manager: DeviceManager = self.device.get_module("device_manager") # type: ignore
        
        self.discovery_port = self.settings_manager.register_setting(domain="discovery", version="V1", setting_name="Discovery Port", default_value="5000", type="int", description="Port to be used for multicast discovery. (Must be the same across all devices)", validation_data={}, user_facing=True)
        self.discovery_multicast_address = self.settings_manager.register_setting(domain="discovery", version="V1", setting_name="Discovery Multicast Address", default_value="239.143.23.9", type="ip", description="Address to be used for multicast discovery. (Must be the same across all devices)", validation_data={"multicast": True}, user_facing=True)
    
        print(self.discovery_port.get_value())
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.sock.setblocking(False)
        self.sock.bind(("0.0.0.0", self.discovery_port.get_value())) # TODO adjust to only bind to private ip ranges for security
        
        group = socket.inet_aton(str(self.discovery_multicast_address.get_value()))
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
    def send_discovery(self) -> None:
        """Send discovery message"""
        
        init_message = {
                "type": "discover",
                "id": self.settings_manager.get_setting("device", "id").get_value(),
                "ver": 1,
                "http": f"http://{self.networking.get_local_ip()}:{5000}/api",
                "ws": f"ws://{self.networking.get_local_ip()}:{5000}/ws",
                "caps": self.api_registery.get_capabilities(),
                "ts": str(datetime.now())
            }
        message = json.dumps(init_message, indent=4).encode()
        
        try:
            self.sock.sendto(message, (str(self.discovery_multicast_address.get_value()), self.discovery_port.get_value()))
            self.api_send_id += 1
            
        except Exception as e:
            print(f"An error ocured when trying to send an auto discovery message: {e}")

    def check_for_discovery(self) -> None:
        """Listen for discovery messages."""
        address = None
        try:
            data, address = self.sock.recvfrom(2048)
            data = json.loads(data.decode())
            self.remotes[data["id"]] = data
            
            #TODO add new devices to device manager
                
        except BlockingIOError:
            return
        
        except ValueError:
            print(f"Invalid Message from {address}")
            
    def update(self, delta_time: float) -> None:
        if time.time() - self.last_send_time > 2:
            self.send_discovery()
            
    
def register(device):
    return "discovery", DiscoveryEngine(device)