"""
Database Module Entrypoint

Part of WebDisplay
System Database Module

License: MIT license

Author: C2311231

Notes:
"""

import src.system_modules.database.settings_manager as settings_manager
import src.module
import src.system_modules.database.database as database

def register(system) -> tuple[str, src.module.module]:
    system.register_module("database_manager", database.DBManager())
    return settings_manager.register(system)