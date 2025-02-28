import threading
import time
import requests
import json
import commons

class PeerManager(commons.BaseClass):
    def __init__(self, networking, db):
        self.devices = []
        self.networking=networking
        self.db = db
        for peer in self.db.getPeers():
            self.devices.append(Device(peer["web_version"], peer["api_version"], peer["web_url"], peer["web_port"], peer["web_encription"], peer["device_name"], peer["device_state"], peer["device_platform"], peer["device_id"], peer["device_ip"], self.db, id=peer["id"]))
            
        threading.Thread(target=self.checkDeviceConnections, daemon=True).start()
        
    def startDiscovery(self):
        threading.Thread(target=self.networking.send_discovery, daemon=True).start()
        threading.Thread(target=self.networking.listen_for_discovery, daemon=True, args=(self.foundDevice, )).start()

    def foundDevice(self, data, address):
        for device in self.devices:
            if device.device_id == data["device_id"]:
                device.pinged()
                device.device_ip = data["device_ip"]
                device.device_name = data["device_name"]
                device.web_port = data["web_port"]
                device.web_url = data["web_url"]
                return
        self.devices.append(Device(data["web_version"], data["api_version"], data["web_url"], data["web_port"], data["web_encription"], data["device_name"], data["device_state"], data["device_platform"], data["device_id"], data["device_ip"], self.db))
        
    def addDevice(self, ip, port):
        request = requests.get("http://" + ip+":"+port + "/api/status/")
        
        if request.ok:
            data = request.json()
            self.devices.append(Device(data["web_version"], data["api_version"], data["web_url"], data["web_port"], data["web_encription"], data["device_name"], data["device_state"], data["device_platform"], data["device_id"], data["device_ip"], self.db))
            return True
        return False
        
    def checkDeviceConnections(self):
        while True:
            for device in self.devices:
                device.checkConection()
                
            time.sleep(5)
            
    
            

class Device():
    def __init__(self, web_version, api_version, web_url, web_port, web_encription, device_name, device_state, device_platform, device_id, device_ip, db, id=0):
        self.lastCommunication = time.time()
        self.available = True
        self.db = db
        if id==0:
            self.id = self.db.createPeer(web_version, api_version, web_url, web_port, web_encription, device_name, device_state, device_platform, device_id, device_ip, False)
        else:
            self.id = id
    @property  # Getter
    def web_version(self):
        return self.getData().web_version
    @property  # Getter
    def api_version(self):
        return self.getData().api_version
    @property  # Getter
    def web_url(self):
        return self.getData().web_url
    @property  # Getter
    def web_port(self):
        return self.getData().web_port
    @property  # Getter
    def web_encription(self):
        return self.getData().web_encription
    @property  # Getter
    def device_name(self):
        return self.getData().device_name
    @property  # Getter
    def device_state(self):
        return self.getData().device_state
    @property  # Getter
    def device_ip(self):
        return self.getData().device_ip
    @property  # Getter
    def device_platform(self):
        return self.getData().device_platform
    @property  # Getter
    def device_id(self):
        return self.getData().device_id
    @property  # Getter
    def disabled(self):
        return self.getData().disabled
    @web_version.setter  # Setter
    def web_version(self, web_version):
        self.db.editPeer(self.id, web_version = web_version)
        
    @api_version.setter  # Setter
    def api_version(self, api_version):
        self.db.editPeer(self.id, api_version = api_version)
        
    @web_url.setter  # Setter
    def web_url(self, web_url):
        self.db.editPeer(self.id, web_url = web_url)
        
    @web_encription.setter  # Setter
    def web_encription(self, web_encription):
        self.db.editPeer(self.id, web_encription = web_encription)
        
    @device_name.setter  # Setter
    def device_name(self, device_name):
        self.db.editPeer(self.id, device_name = device_name)
        
    @device_state.setter  # Setter
    def device_state(self, device_state):
        self.db.editPeer(self.id, web_version = device_state)
        
    @device_ip.setter  # Setter
    def device_ip(self, device_ip):
        self.db.editPeer(self.id, device_ip = device_ip)
        
    @device_platform.setter  # Setter
    def device_platform(self, device_platform):
        self.db.editPeer(self.id, device_platform = device_platform)
        
    @device_id.setter  # Setter
    def device_id(self, device_id):
        self.db.editPeer(self.id, device_id = device_id)
        
    @web_port.setter  # Setter
    def web_port(self, web_port):
        self.db.editPeer(self.id, web_port = web_port)
        
    @disabled.setter  # Setter
    def disabled(self, disabled):
        self.db.editPeer(self.id, disabled = disabled)
        
    
    def pinged(self):
        self.lastCommunication = time.time()
        self.available = True
        
    def ping(self):
        try:
            request = requests.get(self.web_url + "/api/status/")
        
        except:
            return False
        
        if request.ok:
            self.lastCommunication = time.time()
            data = request.json()
            self.device_name = data["device_name"]
            self.web_port = data["web_port"]
            self.web_url = data["web_url"]
            self.web_url = data["web_url"]
            return True
        return False
    
    def checkConection(self):
        if time.time() - self.lastCommunication > 5:
            if(self.ping()):
                self.available = True
            else:
                self.available = False
    def getData(self):
          return self.db.getPeer(self.id)
      
    def syncEvent(self, event, source_uuid):
        if type(event.data) == str:
            data = json.loads(event.data)
        else:
            data = event.data
        data["peers"].remove(self.getData()["device_id"])
        data["peers"].append(source_uuid)
        event.data = data
        sendData = {
            "name": event.name,
            "color": event.color,
            "wkDay": event.wkDay,
            "startTime": event.startTime,
            "endTime": event.endTime,
            "type": event.type,
            "data": data,
            "syncID": event.syncID,
            "id": event.id
        }
        try:
            request = requests.post(self.getData()["web_url"] + "/api/add/schedule/event/", json=sendData)
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):            
                threading.Thread(target=self.syncEventThreaded, args=(sendData,), daemon=True).start()
            
            
        
    def syncEventThreaded(self, event):
        while True:
            try:
                request = requests.post(self.getData()["web_url"] + "/api/add/schedule/event/", json=event)
                return
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):            
                time.sleep(5)
            
    def deleteEvent(self, id):
        try:
            request = requests.get(self.getData()["web_url"] + f"/api/remove/schedule/event/{id}")
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
            threading.Thread(target=self.deleteEventThreaded, args=(id,), daemon=True).start()
            
    def deleteEventThreaded(self, id):
        while True:
            try:
                request = requests.get(self.getData()["web_url"] + f"/api/remove/schedule/event/{id}")
                return
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):            
                time.sleep(5)
                
    def disable(self):
        print("Disabled Peer")
        self.disabled = True
        
    def enable(self):
        print("Enable Peer")
        self.disabled = False