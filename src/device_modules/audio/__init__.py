"""
Audio Module Manager

Part of WebDisplay
Device Audio Module

License: MIT license

Author: C2311231

Notes:
TODO Complete Audio Manager Implementation
"""

from src.device import Device
from src.module import module
disabled = False

#import pulsectl

class AudioManager(module):
    def __init__(self, device_module: Device):
        if disabled:
            return
        self.device_module = device_module
        #self.pulse = pulsectl.Pulse('webdisplay-audio')
        self.audio_devices = []
        
    def start(self):
        super().start()
        
    def register_audio_device(self, audio_device) -> None:
        self.audio_devices.append(audio_device)
        
    def get_audio_devices(self) -> list:
        return self.audio_devices
    
def register(device_module: Device) -> tuple[str, module]:
    return "audio_manager", AudioManager(device_module)