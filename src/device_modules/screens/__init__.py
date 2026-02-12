"""
Screen Module Manager

Part of WebDisplay
Device Screen Module

License: MIT license

Author: C2311231

Notes:
"""

import src.module as module
from src.device import Device

# TODO find a way to get more data on specific ports in use
from screeninfo import get_monitors
from src.device_modules.screens.screen import Screen
from src.device_modules.database.settings_manager import SettingsManager

class ScreenManager(module.module):
    def __init__(self, device: Device):
        self.device = device
        self.screens = []
        self.monitors = get_monitors()[0]
        
    def start(self):
        super().start()
        self.setting_manager: SettingsManager = self.device.get_module("setting_manager") # type: ignore
        domain = "devices." + self.device.device_id + ".screens" 
        existing = self.setting_manager.get_unique_subdomains(domain)
        for screen in existing:
            self.register_screen(Screen.from_db(self.device, screen))
        
    def register_screen(self, screen: Screen) -> None:
        self.screens.append(screen)
        
    def get_screens(self) -> list[Screen]:
        return self.screens
    
def register(device: Device) -> tuple[str, module.module]:
    return "screen_manager", ScreenManager(device)