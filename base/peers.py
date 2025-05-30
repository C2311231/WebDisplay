import threading
import time
import requests
import json
from base import commons, multicast_api_endpoint, networking, database


class PeerManager(commons.BaseClass):
    def __init__(self, networking: networking.NetworkingManager, db: database.Database):
        self.devices = []
        self.discover_engine = multicast_api_endpoint.DiscoveryEngine(db)
        self.networking = networking
        self.db = db
        for peer in self.db.get_peers():
            self.devices.append(
                Device(
                    peer["web_version"],
                    peer["api_version"],
                    peer["web_url"],
                    peer["web_port"],
                    peer["web_encryption"],
                    peer["device_name"],
                    peer["device_state"],
                    peer["device_platform"],
                    peer["device_id"],
                    peer["device_ip"],
                    self.db,
                    id=peer["id"],
                )
            )

        threading.Thread(target=self.check_device_connections, daemon=True).start()

    def start_discovery(self) -> None:
        threading.Thread(target=self.discover_engine.send_discovery, daemon=True).start()
        threading.Thread(
            target=self.discover_engine.listen_for_discovery,
            daemon=True,
            args=(self.found_device,),
        ).start()

    def found_device(self, data) -> None:
        for device in self.devices:
            if device.device_id == data["device_id"]:
                device.pinged()
                device.device_ip = data["device_ip"]
                device.device_name = data["device_name"]
                device.web_port = data["web_port"]
                device.web_url = data["web_url"]
                return
        self.devices.append(
            Device(
                data["web_version"],
                data["api_version"],
                data["web_url"],
                data["web_port"],
                data["web_encryption"],
                data["device_name"],
                data["device_state"],
                data["device_platform"],
                data["device_id"],
                data["device_ip"],
                self.db,
            )
        )

    def add_device(self, ip: commons.Address, port: int) -> None:
        request = requests.get("http://" + str(ip) + ":" + str(port) + "/api/status/")

        if request.ok:
            data = request.json()
            self.devices.append(
                Device(
                    data["web_version"],
                    data["api_version"],
                    data["web_url"],
                    data["web_port"],
                    data["web_encryption"],
                    data["device_name"],
                    data["device_state"],
                    data["device_platform"],
                    data["device_id"],
                    data["device_ip"],
                    self.db,
                )
            )
            return True
        return False

    def check_device_connections(self) -> None:
        while True:
            for device in self.devices:
                device.check_connection()

            time.sleep(5)
            
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
