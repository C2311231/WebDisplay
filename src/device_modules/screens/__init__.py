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

class ScreenManager(module.module):
    def __init__(self, device: Device):
        self.device = device
        self.screens = []
        self.monitors = get_monitors()
        
    def start(self):
        super().start()
        self.data, self.first_init = self.device.config.get_module("screens", default={"screens": []})
        if self.first_init:
            monitors = get_monitors()
            for monitor in monitors:
                self.register_screen(Screen(self.device, str(monitor.name), str(monitor.name), 100, "", "local", 1.0))
            
        else:
            existing = self.data["screens"]
            for screen in existing:
                self.register_screen(Screen.from_config(self.device, screen))
        
    def register_screen(self, screen: Screen) -> None:
        self.screens.append(screen)
        self.data["screens"] = [screen.get_id() for screen in self.screens]
        self.device.config.save_module("screens", self.data)
        
    def get_screens(self) -> list[Screen]:
        return self.screens
    
def register(device: Device) -> tuple[str, module.module]:
    return "screen_manager", ScreenManager(device)