"""
Webdisplay Main Program File

Part of WebDisplay
Entrypoint

License: MIT license

Author: C2311231

Notes:
"""

import src.device as Device
device = Device.Device()
device.load_modules()
device.validate_required_modules()
device.start_modules()

## Start program loop
device.main_loop()