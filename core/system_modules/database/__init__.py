"""
Database Module Entrypoint

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
"""

import core.system_modules.database.settings_manager as settings_manager
import core.module

def register(system) -> tuple[str, core.module.module]:
    return settings_manager.register(system)