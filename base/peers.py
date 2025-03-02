import threading
import time
import requests
import json
from base import commons, networking, database, auto_discovery


class PeerManager(commons.BaseClass):
    def __init__(self, networking: networking.NetworkingManager, db: database.Database):
        self.devices = []
        self.discover_engine = auto_discovery.DiscoveryEngine(db)
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

    def add_device(self, ip: commons.address, port: int) -> None:
        request = requests.get("http://" + ip + ":" + port + "/api/status/")

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


class Device:
    def __init__(
        self,
        web_version,
        api_version,
        web_url,
        web_port,
        web_encryption,
        device_name,
        device_state,
        device_platform,
        device_id,
        device_ip,
        db: database.Database,
        id=0,
    ):
        self.last_communication = time.time()
        self.available = True
        self.db = db
        if id == 0:
            self.id = self.db.create_peer(
                web_version,
                api_version,
                web_url,
                web_port,
                web_encryption,
                device_name,
                device_state,
                device_platform,
                device_id,
                device_ip,
                False,
            )
        else:
            self.id = id

    @property  # Getter
    def web_version(self) -> str:
        return self.get_data().web_version

    @property  # Getter
    def api_version(self) -> str:
        return self.get_data().api_version

    @property  # Getter
    def web_url(self) -> str:
        return self.get_data().web_url

    @property  # Getter
    def web_port(self) -> str:
        return self.get_data().web_port

    @property  # Getter
    def web_encryption(self) -> str:
        return self.get_data().web_encryption

    @property  # Getter
    def device_name(self) -> str:
        return self.get_data().device_name

    @property  # Getter
    def device_state(self) -> str:
        return self.get_data().device_state

    @property  # Getter
    def device_ip(self) -> str:
        return self.get_data().device_ip

    @property  # Getter
    def device_platform(self) -> str:
        return self.get_data().device_platform

    @property  # Getter
    def device_id(self) -> str:
        return self.get_data().device_id

    @property  # Getter
    def disabled(self) -> str:
        return self.get_data().disabled

    @web_version.setter  # Setter
    def web_version(self, web_version) -> None:
        self.db.edit_peer(self.id, web_version=web_version)

    @api_version.setter  # Setter
    def api_version(self, api_version) -> None:
        self.db.edit_peer(self.id, api_version=api_version)

    @web_url.setter  # Setter
    def web_url(self, web_url) -> None:
        self.db.edit_peer(self.id, web_url=web_url)

    @web_encryption.setter  # Setter
    def web_encryption(self, web_encryption) -> None:
        self.db.edit_peer(self.id, web_encryption=web_encryption)

    @device_name.setter  # Setter
    def device_name(self, device_name) -> None:
        self.db.edit_peer(self.id, device_name=device_name)

    @device_state.setter  # Setter
    def device_state(self, device_state) -> None:
        self.db.edit_peer(self.id, web_version=device_state)

    @device_ip.setter  # Setter
    def device_ip(self, device_ip) -> None:
        self.db.edit_peer(self.id, device_ip=device_ip)

    @device_platform.setter  # Setter
    def device_platform(self, device_platform) -> None:
        self.db.edit_peer(self.id, device_platform=device_platform)

    @device_id.setter  # Setter
    def device_id(self, device_id) -> None:
        self.db.edit_peer(self.id, device_id=device_id)

    @web_port.setter  # Setter
    def web_port(self, web_port) -> None:
        self.db.edit_peer(self.id, web_port=web_port)

    @disabled.setter  # Setter
    def disabled(self, disabled) -> None:
        self.db.edit_peer(self.id, disabled=disabled)

    def pinged(self) -> None:
        self.last_communication = time.time()
        self.available = True

    def ping(self) -> bool:
        try:
            request = requests.get(self.web_url + "/api/status/")

        except:
            return False

        if request.ok:
            self.last_communication = time.time()
            data = request.json()
            self.device_name = data["device_name"]
            self.web_port = data["web_port"]
            self.web_url = data["web_url"]
            self.web_url = data["web_url"]
            return True
        return False

    def check_connection(self) -> None:
        if time.time() - self.last_communication > 5:
            if self.ping():
                self.available = True
            else:
                self.available = False

    def get_data(self) -> dict:
        return self.db.get_peer(self.id)

    def sync_event(self, event: object, source_uuid: str) -> None:
        if type(event.data) == str:
            data = json.loads(event.data)
        else:
            data = event.data
        data["peers"].remove(self.get_data()["device_id"])
        data["peers"].append(source_uuid)
        event.data = data
        send_data = {
            "name": event.name,
            "color": event.color,
            "wkDay": event.wkDay,
            "startTime": event.startTime,
            "endTime": event.endTime,
            "type": event.type,
            "data": data,
            "syncID": event.syncID,
            "id": event.id,
        }
        try:
            request = requests.post(
                self.get_data()["web_url"] + "/api/add/schedule/event/", json=send_data
            )
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            threading.Thread(
                target=self.sync_event_threaded, args=(send_data,), daemon=True
            ).start()

    def sync_event_threaded(self, event: object) -> None:
        while True:
            try:
                request = requests.post(
                    self.get_data()["web_url"] + "/api/add/schedule/event/", json=event
                )
                return
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
                time.sleep(5)

    def delete_event(self, id: str) -> None:
        try:
            request = requests.get(
                self.get_data()["web_url"] + f"/api/remove/schedule/event/{id}"
            )
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            threading.Thread(
                target=self.delete_event_threaded, args=(id,), daemon=True
            ).start()

    def delete_event_threaded(self, id: str) -> None:
        while True:
            try:
                request = requests.get(
                    self.get_data()["web_url"] + f"/api/remove/schedule/event/{id}"
                )
                return
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
                time.sleep(5)

    def disable(self) -> None:
        print("Disabled Peer")
        self.disabled = True

    def enable(self) -> None:
        print("Enable Peer")
        self.disabled = False
