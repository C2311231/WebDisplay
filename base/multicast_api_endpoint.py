import socket
import struct
import json
import time
from base import commons, database


class DiscoveryEngine(commons.BaseClass):
    def __init__(
        self,
        config: dict,
        database: database.Database,
        discovery_port: int = 5000,
        discovery_multicast_address: commons.Address = commons.Address("239.143.23.9")
    ):
        if not discovery_multicast_address.is_multicast():
            raise ValueError()
        self.config = config
        self.discovery_port = discovery_port
        self.discovery_multicast_address = discovery_multicast_address
        self.database = database
        self.api_send_id = 0
        
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
                    "source": self.config["device_id"],
                    "domain": "peer_manager",
                    "name": "discovery",
                    "data": {
                        "device_name": self.config["name"],
                        "device_id": self.config["device_id"],
                        "device_ip": self.config["ip"],
                        "device_port": self.config["port"],
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