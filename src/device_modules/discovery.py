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
import src.module
from src.device_modules.networking import NetworkingManager
from datetime import datetime
from src.device_modules.api import APIRegistry

class DiscoveryEngine(src.module.module):
    def __init__(self, device: Device):
        self.device = device
        device.require_modules("networking", "api_registry")
        self.api_send_id = 0
        self.last_send_time = time.time()
        self.remotes = {}
        
    def start(self) -> None:
        self.networking: NetworkingManager = self.device.get_module("networking") # type: ignore
        self.api_registery: APIRegistry = self.device.get_module("api_registry") # type: ignore
        
        self.data, self.first_init = self.device.config.get_module("discovery", default={"Discovery Port": "5000", "Discovery Multicast Address": "239.143.23.9"})
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.sock.setblocking(False)
        self.sock.bind(("0.0.0.0", int(self.data["Discovery Port"]))) # TODO adjust to only bind to private ip ranges for security
        
        group = socket.inet_aton(str(self.data["Discovery Multicast Address"]))
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        
    def save_data(self):
        self.device.config.save_module("discovery", self.data)
        
    def send_discovery(self) -> None:
        """Send discovery message"""
        
        init_message = {
                "type": "discover",
                "id": self.device.data["device_id"],
                "ver": 1,
                "http": f"http://{self.networking.get_local_ip()}:{5000}/api",
                "ws": f"ws://{self.networking.get_local_ip()}:{5000}/ws",
                "caps": self.api_registery.get_capabilities(),
                "ts": str(datetime.now())
            }
        message = json.dumps(init_message, indent=4).encode()
        
        try:
            self.sock.sendto(message, (str(self.data["Discovery Multicast Address"]), int(self.data["Discovery Port"])))
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