"""
Screen Module Screen Class

Part of WebDisplay
Device Screen Module

License: MIT license

Author: C2311231

Notes:
"""

import core.system
import core.system_modules.device_manager.device as device
from core.system_modules.database.setting import Setting
from core.system_modules.database.settings_manager import SettingsManager
import uuid

class Screen():
    def __init__(self, system: core.system.system, device: device.Device, screen_name: str, x: int, y: int, port: str, resolution_x: int, resolution_y: int, volume: float, sound_device: str, screen_type: str, scale: float, screen_id: str = ""):
        self.system = system
        self.device = device
        self.db_manager: SettingsManager = system.get_module("settings_manager") # type: ignore
        
        if screen_id == "":
            screen_id = str(uuid.uuid4())
            
        domain = "devices." + self.device.device_id + ".screens." + screen_id 
        
        self.screen_id = screen_id
        
        self.resolution_x = self.db_manager.register_setting(domain, "V1", "Screen X Resolution", str(resolution_x), "string", "X Resolution for this screen", {}, False).push_to_db()
        self.resolution_y = self.db_manager.register_setting(domain, "V1", "Screen Y Resolution", str(resolution_y), "string", "Y Resolution for this screen", {}, False).push_to_db()
        self.port = self.db_manager.register_setting(domain, "V1", "Screen Port", port, "enum", "Port connected to this screen", {"options": []}, True).push_to_db()
        self.scale = self.db_manager.register_setting(domain, "V1", "Screen Scale", str(scale), "float", "Scaling factor for this screen", {"min_value": 0, "max_value": 4}, True).push_to_db()
        self.screen_name = self.db_manager.register_setting(domain, "V1", "Screen Name", screen_name, "string", "Name for this screen", {}, True).push_to_db()
        self.volume = self.db_manager.register_setting(domain, "V1", "Screen Volume", str(volume), "float", "Volume for this screen", {"min_value": 0, "max_value": 1}, True).push_to_db()
        self.sound_device = self.db_manager.register_setting(domain, "V1", "Screen Audio Device", sound_device, "enum", "Audio output for this screen", {"options": []}, True).push_to_db()
        self.screen_type = self.db_manager.register_setting(domain, "V1", "Screen Type", screen_type, "enum", "Type for this screen", {"options": ["Local", "Remote"]}, True).push_to_db()
        self.active = False
        self.locked = False
        self.x = self.db_manager.register_setting(domain, "V1", "Screen Location X", str(x), "enum", "X location of this screen", {}, False).push_to_db()
        self.y = self.db_manager.register_setting(domain, "V1", "Screen Location Y", str(y), "enum", "Y location of this screen", {}, False).push_to_db()
        
    @classmethod
    def from_db(cls, system: core.system.system, device: device.Device, screen_id: str):
        """
        Generates an existing screen from the db

        Args:
            system (core.system.system): _description_
            device (device.Device): _description_
            screen_id (str): _description_
        """        
        return cls(system, device, "", 0, 0, "", 0, 0, 0, "", "", 0, screen_id)
        
    def set_active(self, active: bool) -> None:
        self.active = active
        
    def is_active(self) -> bool:
        return self.active
    
    def lock(self) -> None:
        self.locked = True
        
    def release(self) -> None:
        self.locked = False
        
    def get_x(self) -> int:
        return self.x.get_value() # type: ignore
    
    def get_y(self) -> int:
        return self.y.get_value() # type: ignore
    
    def get_resolution(self) -> tuple[int, int]:
        return (self.resolution_x.get_value(), self.resolution_y.get_value()) # type: ignore
    
    def get_port(self) -> str:
        return self.port.get_value() # type: ignore
    
    def get_scale(self) -> float:
        return self.scale.get_value() # type: ignore
    
    def get_name(self) -> str:
        return self.screen_name.get_value() # type: ignore
    
    def get_id(self) -> str:
        return self.screen_id
    
    def get_type(self) -> str:
        return self.screen_type.get_value() # type: ignore
    
    def get_sound_device(self) -> str:
        return self.sound_device.get_value() # type: ignore
    
    def get_volume(self) -> float:
        return self.volume.get_value() # type: ignore