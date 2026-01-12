"""
Content Module Base Class

Part of WebDisplay
Device Content Module

License: MIT license

Author: C2311231

Notes:
"""

import core.system as system
import core.system_modules.device_manager.device as device
import core.system_modules.device_manager.device_modules.screens as device_manager_screen

# TODO Store Content in Database

class Content:
    def __init__(self, system: system.system, device: device.Device):
        self.device = device
        self.system = system
        
    def start_content(self, screen: device_manager_screen.Screen):
        pass
    
    def stop_display(self):
        pass
    
    def get_status(self):
        pass
    
    def update_content(self, content_data: dict):
        pass
    
    def preview(self):
        pass