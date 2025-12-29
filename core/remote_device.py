import device
class RemoteDevice(device.Device):
    __mapper_args__ = {
        "polymorphic_identity": "remote",
    }