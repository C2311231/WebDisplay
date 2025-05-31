import threading
import time
import requests
import json
import api_v2
from base import commons, multicast_api_endpoint, networking, database


class PeerManager(commons.BaseClass):
    def __init__(self, networking: networking.NetworkingManager, db: database.Database):
        self.discover_engine = multicast_api_endpoint.DiscoveryEngine(db)
        self.networking = networking
        self.db = db
        threading.Thread(target=self.check_device_connections, daemon=True).start()

    def start_discovery(self) -> None:
        threading.Thread(target=self.discover_engine.send_discovery, daemon=True).start()
        threading.Thread(
            target=self.discover_engine.listen_for_discovery,
            daemon=True,
            args=(self.found_device,),
        ).start()

    def found_device(self, device_id:str, device_ip: str, device_port: int) -> None:
        peer = self.db.get_peer(device_id)
        if peer:
            peer.update_ip(device_ip)
            peer.device_port = device_port
            self.db.db.session.commit()
        else:
            self.add_device(commons.Address(device_ip), device_id, device_port)
        
    def add_device(self, ip: commons.Address, device_id: str, port: int) -> None:
        device_name = api_v2.call_http_api(str(ip), port, "get", device_id, "database", "get_config_entry", {"parameter": "device_name"})
        device_groups = api_v2.call_http_api(str(ip), port, "get", device_id, "database", "get_config_entry", {"parameter": "device_groups"})
        if device_name.error == False and device_groups.error == False:
            self.db.write_peer(device_name=device_name.data["value"], device_id=device_id, device_ip=str(ip), groups=device_groups.data["value"])

    def check_device_connections(self) -> None:
        while True:
            for device in self.db.get_peers():
                device.ping(self.db.get_config_entry("device_id"))

            time.sleep(5)
            
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
