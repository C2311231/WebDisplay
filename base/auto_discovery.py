import socket
import struct
import json
import time
from base import commons, database


class DiscoveryEngine(commons.BaseClass):
    def __init__(
        self,
        database: database,
        discovery_port: int = 5000,
        discovery_multicast_address: commons.address = commons.address("239.143.23.9")
    ):
        if not discovery_multicast_address.is_multicast():
            raise ValueError()

        self.discovery_port = discovery_port
        self.discovery_multicast_address = discovery_multicast_address
        self.database = database
        
    def send_discovery(self) -> None:
        """Send discovery message periodically."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(
            socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2
        )  # Set TTL to 2 for local network

        while True:
            init_message = {
                "web_version": self.database.config()["web_version"],
                "api_version": self.database.config()["api_version"],
                "web_url": self.database.config()["url"],
                "web_port": self.database.config()["port"],
                "web_encryption": self.database.config()["encryption"],
                "device_name": self.database.config()["name"],
                "device_state": self.database.config()["state"],
                "device_platform": self.database.config()["platform"],
                "device_id": self.database.config()["id"],
                "device_ip": self.database.config()["ip"],
            }
            message = json.dumps(init_message, indent=4).encode()
            sock.sendto(
                message, (self.discovery_multicast_address, self.discovery_port)
            )
            time.sleep(5)  # Send every 5 seconds

    def listen_for_discovery(self, callback: function) -> None:
        """Listen for discovery messages."""
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(("", self.discovery_port))

        group = socket.inet_aton(self.discovery_multicast_address)
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        init_message = {
            "web_version": self.database.config()["web_version"],
            "api_version": self.database.config()["api_version"],
            "web_url": self.database.config()["url"],
            "web_port": self.database.config()["port"],
            "web_encryption": self.database.config()["encryption"],
            "device_name": self.database.config()["name"],
            "device_state": self.database.config()["state"],
            "device_platform": self.database.config()["platform"],
            "device_id": self.database.config()["id"],
            "device_ip": self.database.config()["ip"],
        }

        while True:
            data, address = sock.recvfrom(1024)

            try:
                data = json.loads(data.decode())
                if data["device_id"] == self.database.config()["id"]:
                    continue
                if data.keys() == init_message.keys():

                    callback(data, address)
            except ValueError:
                print(f"Invalid Message from {address}")

    def tick(self) -> None:
        # Run any maintenance tasks and checks (about every 5 seconds)
        pass

    def required_config() -> dict:
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
