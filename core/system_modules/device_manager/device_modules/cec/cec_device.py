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

import glob

cec_ports = glob.glob("/dev/cec*")
print("Found CEC adapters:", cec_ports)



#cec = None  # clears problems in ide (no affect on code)
from core import commons

try:
    import cec
except:
    pass

class CecManager(commons.BaseClass):
    def __init__(self) -> None:
        """Initializes the CEC manager."""
        try:
            cec.init() # type: ignore
            self.devices = cec.list_devices() # type: ignore
            self.tv = cec.Device(cec.CECDEVICE_TV) # type: ignore
            device_name = "WebDisplay" # (max 13 ASCII chars for standard)
            parameters = device_name.encode('ascii')
            cec.transmit(cec.CECDEVICE_TV, cec.CEC_OPCODE_SET_OSD_NAME, parameters) # type: ignore
            
            self.tv.is_on()
            self.disable_cec = False
        except:
            print("CEC Unavailable")
            self.disable_cec = True

    def tv_on(self) -> commons.Response:
        """Turns on the TV using CEC."""
        if not self.disable_cec:
            try:
                self.tv.power_on()
                print("Tv Power On")
                return commons.Response(False, "success", "Tv power On", 200, {})
            except Exception as e:
                print(e)
                return commons.Response(
                    True, "failed", f"Unexpected error: {e}", 500, {}
                )
        print("CEC Power On Unavailable")
        return commons.Response(True, "failed", "CEC Unavailable", 503, {})

    def tv_off(self) -> commons.Response:
        """Turns off the TV using CEC."""
        if not self.disable_cec:
            try:
                self.tv.standby()
                print("Tv Power Off")
                return commons.Response(False, "success", "Tv power Off", 200, {})
            except Exception as e:
                print(e)
                return commons.Response(
                    True, "failed", f"Unexpected error: {e}", 500, {}
                )
        print("CEC Power Off Unavailable")
        return commons.Response(True, "failed", "CEC Unavailable", 503, {})

    def get_tv_power(self) -> bool:
        if not self.disable_cec:
            return self.tv.is_on()
        return False

    def set_active(self) -> commons.Response:
        """Sets device as active using CEC."""
        if not self.disable_cec:
            try:
                cec.set_active_source() # type: ignore
                print("Tv Active Source Set")
                return commons.Response(False, "success", "Active Source Set", 200, {})
            except Exception as e:
                print(e)
                return commons.Response(
                    True, "failed", f"Unexpected error: {e}", 500, {}
                )
        print("CEC Set Active Unavailable")
        return commons.Response(True, "failed", "CEC Unavailable", 503, {})

    def volume_up(self) -> commons.Response:
        """Increases volume using cec."""
        if not self.disable_cec:
            try:
                cec.volume_up() # type: ignore
                print("Tv Volume Up")
                return commons.Response(False, "success", "Volume Up", 200, {})
            except Exception as e:
                print(e)
                return commons.Response(
                    True, "failed", f"Unexpected error: {e}", 500, {}
                )
        print("CEC Volume Up Unavailable")
        return commons.Response(True, "failed", "CEC Unavailable", 503, {})

    def volume_down(self) -> commons.Response:
        """Decreases volume using cec."""
        if not self.disable_cec:
            try:
                cec.volume_down() # type: ignore
                print("Tv Volume Down")
                return commons.Response(False, "success", "Volume Down", 200, {})
            except Exception as e:
                print(e)
                return commons.Response(
                    True, "failed", f"Unexpected error: {e}", 500, {}
                )
        print("CEC Volume Down Unavailable")
        return commons.Response(True, "failed", "CEC Unavailable", 503, {})

    def toggle_mute(self) -> commons.Response:
        """Toggles volume mute using cec."""
        if not self.disable_cec:
            try:
                cec.toggle_mute() # type: ignore
                print("Tv toggle Mute")
                return commons.Response(False, "success", "Mute Toggled", 200, {})
            except Exception as e:
                print(e)
                return commons.Response(
                    True, "failed", f"Unexpected error: {e}", 500, {}
                )
        print("CEC toggle mute Unavailable")
        return commons.Response(True, "failed", "CEC Unavailable", 503, {})

    def get_vender(self) -> str:
        if not self.disable_cec:
            try:
                return venderDecoder[self.tv.vendor]
            except:
                return "UNKNOWN"
        return "UNKNOWN"