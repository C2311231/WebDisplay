import core.system_modules.device_manager.device as device
class RemoteDevice(device.Device):
    __mapper_args__ = {
        "polymorphic_identity": "remote",
    }