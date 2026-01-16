"""
Device Manager Module Local Device Class

Part of WebDisplay
System device_manager Module

License: MIT license

Author: C2311231

Notes:
"""

import core.system_modules.device_manager.device as device
import pkgutil
import importlib
import core.system_modules.device_manager.device_modules as device_modules
import core.module as Module
import time

class LocalDevice(device.Device):
    modules = {}
    __mapper_args__ = {
        "polymorphic_identity": "local",
    }
    
    def __init__(self, system, **kwargs):
        self.system = system
        self.load_modules()
        self.required_modules = []
        super().__init__(**kwargs)
        
    def load_modules(self):
        for _, module_name, _ in pkgutil.iter_modules(device_modules.__path__):
            module = importlib.import_module(f"{device_modules.__name__}.{module_name}")

            if hasattr(module, "register"):
                module_id, module = module.register(self, self.system)
                
                if module_id in self.modules:
                    raise ValueError(f"Module with id {module_id} is already registered.")

                if not isinstance(module, Module.module):
                    raise TypeError(f"{module_id} does not inherit module")

                self.modules[module_id] = module
            else:
                raise ValueError(f"Module {module_name} does not have a register function.")
                
                
    def get_module(self, module_id: str):
        if module_id not in self.modules:
            raise KeyError(f"Module with id {module_id} not found on device.")
        return self.modules.get(module_id)
    
    def get_all_modules(self):
        return self.modules
    
    def module_exists(self, module_id: str) -> bool:
        return module_id in self.modules
    
    def update_modules(self):
        for module_id, module in self.modules.items():
            if hasattr(module, "update"):
                module.update(time.time()-self._last_update_time)
            self._last_update_time = time.time()
    
    def start_modules(self):
        for module_id, module in self.modules.items():
            if hasattr(module, "start"):
                module.start()
                
    def shutdown_modules(self):
        for module_id, module in self.modules.items():
            if hasattr(module, "shutdown"):
                module.shutdown()
                
                
    def require_module(self, module_id: str):
        self.required_modules.append(module_id)

    def require_modules(self, *module_ids: str):
        for module_id in module_ids:
            self.require_module(module_id)
            
    def validate_required_modules(self):
        for module_id in self.required_modules:
            if module_id not in self.modules:
                raise ValueError(f"Required module {module_id} not loaded in device.")