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

import ipaddress
import json
import socket
import struct
import time
from datetime import datetime

import src.module
from src.device import Device
from src.device_modules.api import APIRegistry
from src.device_modules.networking import NetworkingManager


class DiscoveryEngine(src.module.module):
    def __init__(self, device: Device):
        self.device = device
        device.require_modules("networking", "api_registry")
        self.api_send_id = 0
        self.last_send_time = time.time()
        self.remotes = {}

    def start(self) -> None:
        port = int(self.data["Discovery Port"])
        mcast_addr = str(self.data["Discovery Multicast Address"])

        self.networking: NetworkingManager = self.device.get_module("networking")  # type: ignore
        self.api_registery: APIRegistry = self.device.get_module("api_registry")  # type: ignore

        self.data, self.first_init = self.device.config.get_module(
            "discovery",
            default={
                "Discovery Port": "5000",
                "Discovery Multicast Address": "239.143.23.9",
            },
        )

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        self.sock.setblocking(False)
        self.sock.bind(("0.0.0.0", port))

        for addrinfo in socket.getaddrinfo(socket.gethostname(), None):
            ip = addrinfo[4][0]
            try:
                ip_obj = ipaddress.ip_address(ip)
                if ip_obj.is_private and ip_obj.version == 4:
                    group = socket.inet_aton(mcast_addr)
                    iface = socket.inet_aton(str(ip))
                    mreq = struct.pack("4s4s", group, iface)
                    self.sock.setsockopt(
                        socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq
                    )
                    print(f"Joined multicast group {mcast_addr} on {ip}")
            except ValueError:
                continue

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
            "ts": str(datetime.now()),
        }
        message = json.dumps(init_message, indent=4).encode()

        try:
            self.sock.sendto(
                message,
                (
                    str(self.data["Discovery Multicast Address"]),
                    int(self.data["Discovery Port"]),
                ),
            )
            self.api_send_id += 1

        except Exception as e:
            print(f"An error ocured when trying to send an auto discovery message: {e}")

    def update(self, delta_time: float) -> None:
        if time.time() - self.last_send_time > 2:
            self.send_discovery()


def register(device):
    return "discovery", DiscoveryEngine(device)
