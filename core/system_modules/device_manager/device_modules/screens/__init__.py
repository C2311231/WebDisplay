"""
Screen Module Manager

Part of WebDisplay
Device Screen Module

License: MIT license

Author: C2311231

Notes:
"""

import core.module as device_module
import core.system as system
from core.system_modules.device_manager.device_modules.screens.screen import Screen

class ScreenManager(device_module.module):
    def __init__(self, device_module: device_module.module, system: system.system):
        self.device_module = device_module
        self.system = system
        self.screens = []
        
    def start(self):
        super().start()
        
    def register_screen(self, screen: Screen) -> None:
        self.screens.append(screen)
        
    def get_screens(self) -> list[Screen]:
        return self.screens
    
def register(device_module: device_module.module, system: system.system) -> tuple[str, device_module.module]:
    return "screen_manager", ScreenManager(device_module, system)