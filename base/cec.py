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

cec = None  # clears problems in ide (no affect on code)
from base import commons
try:
    import cec
except:
    pass
class CecManager(commons.BaseClass):
    def __init__(self):
        try:
            cec.init()
            self.devices = cec.list_devices()
            self.tv = cec.Device(cec.CECDEVICE_TV)
            self.tv.is_on()
            self.disable_cec = False
        except:
            print("CEC Unavailable")
            self.disable_cec = True

    def tv_on(self) -> None:
        if not self.disable_cec:
            try:
                self.tv.power_on()
            except Exception as e:
                print(e)
        print("Tv On")

    def tv_off(self) -> None:
        if not self.disable_cec:
            try:
                self.tv.standby()
            except Exception as e:
                print(e)
        print("Tv Off")

    def get_tv_power(self) -> bool:
        if not self.disable_cec:
            return self.tv.is_on()
        return False

    def set_active(self) -> None:
        if not self.disable_cec:
            try:
                cec.set_active_source()
            except Exception as e:
                print(e)
        print("Active")

    def volume_up(self) -> None:
        if not self.disable_cec:
            try:
                cec.volume_up()
            except Exception as e:
                print(e)
        print("Volume Up")

    def volume_down(self) -> None:
        if not self.disable_cec:
            try:
                cec.volume_down()
            except Exception as e:
                print(e)
        print("Volume Down")

    def toggle_mute(self) -> None:
        if not self.disable_cec:
            try:
                cec.toggle_mute()
            except Exception as e:
                print(e)
        print("Volume Mute")

    def get_vender(self) -> str:
        if not self.disable_cec:
            try:
                return venderDecoder[self.tv.vendor]
            except:
                return "UNKNOWN"
        return "UNKNOWN"
