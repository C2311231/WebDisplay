import threading
import time
import requests
import json
from base import commons


class PeerManager(commons.BaseClass):
    def __init__(self, networking, db):
        self.devices = []
        self.networking = networking
        self.db = db
        for peer in self.db.getPeers():
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

    def start_discovery(self):
        threading.Thread(target=self.networking.send_discovery, daemon=True).start()
        threading.Thread(
            target=self.networking.listen_for_discovery,
            daemon=True,
            args=(self.foundDevice,),
        ).start()

    def found_device(self, data, address):
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

    def add_device(self, ip, port):
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

    def check_device_connections(self):
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
        db,
        id=0,
    ):
        self.last_communication = time.time()
        self.available = True
        self.db = db
        if id == 0:
            self.id = self.db.createPeer(
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
    def web_version(self):
        return self.get_data().web_version

    @property  # Getter
    def api_version(self):
        return self.get_data().api_version

    @property  # Getter
    def web_url(self):
        return self.get_data().web_url

    @property  # Getter
    def web_port(self):
        return self.get_data().web_port

    @property  # Getter
    def web_encryption(self):
        return self.get_data().web_encryption

    @property  # Getter
    def device_name(self):
        return self.get_data().device_name

    @property  # Getter
    def device_state(self):
        return self.get_data().device_state

    @property  # Getter
    def device_ip(self):
        return self.get_data().device_ip

    @property  # Getter
    def device_platform(self):
        return self.get_data().device_platform

    @property  # Getter
    def device_id(self):
        return self.get_data().device_id

    @property  # Getter
    def disabled(self):
        return self.get_data().disabled

    @web_version.setter  # Setter
    def web_version(self, web_version):
        self.db.editPeer(self.id, web_version=web_version)

    @api_version.setter  # Setter
    def api_version(self, api_version):
        self.db.editPeer(self.id, api_version=api_version)

    @web_url.setter  # Setter
    def web_url(self, web_url):
        self.db.editPeer(self.id, web_url=web_url)

    @web_encryption.setter  # Setter
    def web_encryption(self, web_encryption):
        self.db.editPeer(self.id, web_encryption=web_encryption)

    @device_name.setter  # Setter
    def device_name(self, device_name):
        self.db.editPeer(self.id, device_name=device_name)

    @device_state.setter  # Setter
    def device_state(self, device_state):
        self.db.editPeer(self.id, web_version=device_state)

    @device_ip.setter  # Setter
    def device_ip(self, device_ip):
        self.db.editPeer(self.id, device_ip=device_ip)

    @device_platform.setter  # Setter
    def device_platform(self, device_platform):
        self.db.editPeer(self.id, device_platform=device_platform)

    @device_id.setter  # Setter
    def device_id(self, device_id):
        self.db.editPeer(self.id, device_id=device_id)

    @web_port.setter  # Setter
    def web_port(self, web_port):
        self.db.editPeer(self.id, web_port=web_port)

    @disabled.setter  # Setter
    def disabled(self, disabled):
        self.db.editPeer(self.id, disabled=disabled)

    def pinged(self):
        self.last_communication = time.time()
        self.available = True

    def ping(self):
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

    def check_connection(self):
        if time.time() - self.last_communication > 5:
            if self.ping():
                self.available = True
            else:
                self.available = False

    def get_data(self):
        return self.db.get_peer(self.id)

    def sync_event(self, event, source_uuid):
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

    def sync_event_threaded(self, event):
        while True:
            try:
                request = requests.post(
                    self.get_data()["web_url"] + "/api/add/schedule/event/", json=event
                )
                return
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
                time.sleep(5)

    def delete_event(self, id):
        try:
            request = requests.get(
                self.get_data()["web_url"] + f"/api/remove/schedule/event/{id}"
            )
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            threading.Thread(
                target=self.delete_event_threaded, args=(id,), daemon=True
            ).start()

    def delete_event_threaded(self, id):
        while True:
            try:
                request = requests.get(
                    self.get_data()["web_url"] + f"/api/remove/schedule/event/{id}"
                )
                return
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
                time.sleep(5)

    def disable(self):
        print("Disabled Peer")
        self.disabled = True

    def enable(self):
        print("Enable Peer")
        self.disabled = False
