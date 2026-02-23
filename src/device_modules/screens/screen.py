"""
Screen Module Screen Class

Part of WebDisplay
Device Screen Module

License: MIT license

Author: C2311231

Notes:
"""

from src.device import Device 
import uuid

class Screen():
    def __init__(self, device: Device, screen_name: str, port: str, volume: float, sound_device: str, screen_type: str, scale: float, screen_id: str = ""):
        self.device = device
        self.device = device
        
        if screen_id == "":
            screen_id = str(uuid.uuid4())
            
        self.data, self.first_init = self.device.config.get_module("screens_" + screen_id, default={
                "screen_name": screen_name,
                "port": port,
                "volume": str(volume),
                "sound_device": sound_device,
                "screen_type": screen_type,
                "scale": str(scale),
                "screen_id": screen_id,
                "enabled": True,
        })
        self.active = False
        self.save_data()
        
    def save_data(self):
        self.device.config.save_module("screens_" + self.get_id(), self.data)
        
    @classmethod
    def from_config(cls, device: Device, screen_id: str):
        data, first_init = device.config.get_module("screens_" + screen_id)
        if first_init:
            raise ValueError(f"Screen with id {screen_id} not found in config.")
        return cls(device, data["screen_name"], data["port"], float(data["volume"]), data["sound_device"], data["screen_type"], float(data["scale"]), screen_id)
        
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
        return self.data["screen_id"]
    
    def get_type(self) -> str:
        return self.screen_type.get_value() # type: ignore
    
    def get_sound_device(self) -> str:
        return self.sound_device.get_value() # type: ignore
    
    def get_volume(self) -> float:
        return self.volume.get_value() # type: ignore