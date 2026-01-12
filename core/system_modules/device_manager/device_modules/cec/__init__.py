"""
CEC Module Manager

Part of WebDisplay
Device CEC Module

License: MIT license

Author: C2311231

Notes:
"""

import glob
import core.module as device_module
import core.system as system
from core.system_modules.device_manager.device_modules.cec.cec_device import CecDevice

class CecManager(device_module.module):
    def __init__(self, device_module: device_module.module, system: system.system):
        self.device_module = device_module
        self.system = system
        self.cec_devices: list[CecDevice] = []
        self.cec_ports = glob.glob("/dev/cec*") # TODO add windows support

    def get_cec_ports(self) -> list[str]:
        return self.cec_ports
    
    def register_cec_device(self, cec_device: CecDevice) -> None:
        self.cec_devices.append(cec_device)
        
    def get_cec_devices(self) -> list[CecDevice]:
        return self.cec_devices
    
def register(system: system.system, device_module: device_module.module):
    cec_manager = CecManager(device_module, system)
    return "cec_manager", cec_manager