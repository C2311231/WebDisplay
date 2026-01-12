"""
Device Manager Module Remote Device Class

Part of WebDisplay
System device_manager Module

License: MIT license

Author: C2311231

Notes:
"""

import core.system_modules.device_manager.device as device

# TODO Use API Registry and endpoint system to manage remote devices via api automatically
class RemoteDevice(device.Device):
    __mapper_args__ = {
        "polymorphic_identity": "remote",
    }