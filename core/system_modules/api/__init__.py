"""
API module entrypoint for managing system interfaces.

Part of WebDisplay
System API Module

License: MIT license

Author: C2311231

Notes:
"""


import core.system_modules.api.api_registry as api_registry
import core.system as system
import core.module as module

def register(system: system.system) -> tuple[str, module.module]:
    return api_registry.register(system)