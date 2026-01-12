"""
System Module

Part of WebDisplay
System

License: MIT license

Author: C2311231

Notes:
"""

import pkgutil
import importlib
import core.system_modules
import time
import core.module as module_base


class system:
    def __init__(self):
        self.modules = {}
        self._last_update_time = time.time()
        self.required_modules = []
        self.running = True
        
    def register_module(self, module):
        module_id, module = module.register(self)
        if module_id in self.modules:
            raise ValueError(f"Module with id {module_id} is already registered.")

        if not isinstance(module, module):
            raise TypeError(f"{module_id} does not inherit module")

        self.modules[module_id] = module
    
    def shutdown(self):
        self.runnuing = False
    
    def load_modules(self):
        for _, module_name, _ in pkgutil.iter_modules(core.system_modules.__path__):
            module = importlib.import_module(f"{core.system_modules.__name__}.{module_name}")

            if hasattr(module, "register"):
                module_id, module = module.register(self)
                
                if module_id in self.modules:
                    raise ValueError(f"Module with id {module_id} is already registered.")

                if not isinstance(module, module_base.module):
                    raise TypeError(f"{module_id} does not inherit module")

                self.modules[module_id] = module
            else:
                raise ValueError(f"Module {module_name} does not have a register function.")
                
                
    def get_module(self, module_id: str):
        if module_id not in self.modules:
            raise KeyError(f"Module with id {module_id} not found. Available modules: {list(self.modules.keys())}")
        return self.modules.get(module_id)
    
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
                raise ValueError(f"Required module {module_id} not loaded in system.")
            
    def core_loop(self):
        while self.running:
            #print("Core Loop Tick")
            self.update_modules()
            time.sleep(0.01) ## Allows other threads to run if they are implmented
            
        self.shutdown_modules()
        exit(0)