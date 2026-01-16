"""
Device Manager Module

Part of WebDisplay
System device_manager Module

License: MIT license

Author: C2311231

Notes:
"""

import core.module as module
import core.system as system
import core.system_modules.device_manager.local_device as local_device
import core.system_modules.device_manager.remote_device as remote_device
import core.system_modules.device_manager.device as device
from sqlalchemy.orm import Session

class DeviceManager(module.module):
    def __init__(self, system: system.system):
        self.system = system
        system.require_modules("database_manager")
        
    def start(self):
        self.database_manager: database.DatabaseManager = self.system.get_module("database_manager")  # type: ignore
        devices = self.get_all_devices()
        for dev in devices:
            dev.register_system(self.system)
            dev.load_modules()
        super().start()
        
        #TODO Remove this after testing
        local_device.LocalDevice(self.system, id=1, device_id="test", device_name="TestDevice")
        
        
    def register_device(self, device: device.Device) -> None:
        self.database_manager.get_session().add(device)
        self.database_manager.get_session().commit()

    def get_device(self, device_id: str) -> device.Device | None:
        return self.database_manager.get_session().query(device.Device).filter_by(device_id=device_id).first()
            
    def get_local_devices(self) -> list:
        return self.database_manager.get_session().query(local_device.LocalDevice).all()
    
    def get_remote_devices(self) -> list:
        return self.database_manager.get_session().query(remote_device.RemoteDevice).all()
    
    def get_all_devices(self) -> list:
        return self.database_manager.get_session().query(device.Device).all()
            
def register(system: system.system) -> tuple[str, module.module]:
    return "device_manager", DeviceManager(system)