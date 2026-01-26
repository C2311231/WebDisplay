"""
CEC Module Class

Part of WebDisplay
Device CEC Module

License: MIT license

Author: C2311231

Notes:
- Manages CEC functionality for a specific HDMI port on supported devices.
- Requires libcec to be installed on the host system.
- Requires proper permissions to access /dev/cec* devices on Linux systems.
- Requires custom fork of python-cec with multi-adapter support: https://github.com/C2311231/python-cec
"""

venderDecoder = {
    0x000039: "TOSHIBA",
    0x0000F0: "SAMSUNG",
    0x0005CD: "DENON",
    0x000678: "MARANTZ",
    0x000982: "LOEWE",
    0x0009B0: "ONKYO",
    0x000CB8: "MEDION",
    0x000CE7: "TOSHIBA",
    0x0010FA: "APPLE",
    0x001582: "PULSE_EIGHT",
    0x001950: "HARMAN_KARDON",
    0x001A11: "GOOGLE",
    0x0020C7: "AKAI",
    0x002467: "AOC",
    0x008045: "PANASONIC",
    0x00903E: "PHILIPS",
    0x009053: "DAEWOO",
    0x00A0DE: "YAMAHA",
    0x00D0D5: "GRUNDIG",
    0x00E036: "PIONEER",
    0x00E091: "LG",
    0x08001F: "SHARP",
    0x080046: "SONY",
    0x18C086: "BROADCOM",
    0x534850: "SHARP",
    0x6B746D: "VIZIO",
    0x8065E9: "BENQ",
    0x9C645E: "HARMAN_KARDON",
    0: "UNKNOWN",
}

from src import system
from src.system_modules.device_manager.device_modules.screens.screen import Screen
from src.system_modules.device_manager.device import Device

try:
    import cec  # type: ignore
except:
    pass

# TODO Add in proper error handling and failure recovery
# # type: ignore is present to suppress ide warnings when cec library is not installed 
class CecDevice():
    def __init__(self, system: system.system, device: Device, screen: Screen, adapter) -> None:
        self.system = system
        self.device = device
        self.screen = screen
        self.adapter = cec.Adapter() # type: ignore
        self.adapter.open(adapter) # type: ignore
        self.devices = self.adapter.list_devices() # type: ignore
        self.tv = self.devices[cec.CECDEVICE_TV] # type: ignore
        self.adapter.set_osd_string(0, "WebDisplay", 0) # type: ignore
        self.disable_cec = False
        self.tv_power = self.tv.is_on() # type: ignore

    def tv_on(self):
        """Turns on the TV using CEC."""
        if not self.disable_cec:
            self.tv.power_on()
            print("Tv Power On")
            return
            
        print("CEC Power On Unavailable")
        
    def update(self, delta_time: float):
        if self.tv_power != self.screen.active:
            if self.screen.active:
                self.tv_on()
                self.set_active()
            else:
                self.tv_off()
            self.tv_power = self.screen.active
            
    def tv_off(self):
        """Turns off the TV using CEC."""
        if not self.disable_cec:
            self.tv.standby()
            print("Tv Power Off")
            return
        
        print("CEC Power Off Unavailable")

    def get_tv_power(self) -> bool:
        if not self.disable_cec:
            return self.tv.is_on()
        return False

    def set_active(self):
        """Sets device as active using CEC."""
        if not self.disable_cec:
            self.adapter.set_active_source() # type: ignore
            print("Tv Active Source Set")
            return
        
        print("CEC Set Active Unavailable")

    def volume_up(self):
        """Increases volume using cec."""
        if not self.disable_cec:
                cec.volume_up() # type: ignore
                print("Tv Volume Up")
                return
            
        print("CEC Volume Up Unavailable")

    def volume_down(self):
        """Decreases volume using cec."""
        if not self.disable_cec:
                self.adapter.volume_down() # type: ignore
                print("Tv Volume Down")
                return
            
        print("CEC Volume Down Unavailable")

    def toggle_mute(self):
        """Toggles volume mute using cec."""
        if not self.disable_cec:
            self.adapter.toggle_mute() # type: ignore
            print("Tv toggle Mute")
            return
        
        print("CEC toggle mute Unavailable")

    def get_vender(self) -> str:
        if not self.disable_cec:
            return venderDecoder[self.tv.vendor]
        return "UNKNOWN"