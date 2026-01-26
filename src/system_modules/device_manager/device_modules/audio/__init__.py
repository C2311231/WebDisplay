"""
Audio Module Manager

Part of WebDisplay
Device Audio Module

License: MIT license

Author: C2311231

Notes:
TODO Complete Audio Manager Implementation
"""

import src.module as device_module
import src.system as system
disabled = False

#import pulsectl

class AudioManager(device_module.module):
    def __init__(self, device_module: device_module.module, system: system.system):
        if disabled:
            return
        self.device_module = device_module
        self.system = system
        #self.pulse = pulsectl.Pulse('webdisplay-audio')
        self.audio_devices = []
        
    def start(self):
        super().start()
        
    def register_audio_device(self, audio_device) -> None:
        self.audio_devices.append(audio_device)
        
    def get_audio_devices(self) -> list:
        return self.audio_devices
    
def register(device_module: device_module.module, system: system.system) -> tuple[str, device_module.module]:
    return "audio_manager", AudioManager(device_module, system)