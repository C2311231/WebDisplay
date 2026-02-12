"""
Device Module Device Base Class

Part of WebDisplay
System device_manager Module

License: MIT license

Author: C2311231

Notes:
"""

import datetime
from sqlalchemy import String, JSON, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.device_modules.database.extentions import db # TODO Find a way to validate this module exists (Or just make a system requried module handler)
from sqlalchemy.ext.mutable import MutableDict
import pkgutil
import src.device_modules as device_modules
import importlib
import src.module as Module
import time

class Device(db):
    __tablename__ = "device"
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    device_type: Mapped[str] = mapped_column(String(20), nullable=False)  # discriminator
    device_name: Mapped[str] = mapped_column(nullable=False)
    created_at = mapped_column(DateTime, nullable=False, default=datetime.datetime.now(datetime.timezone.utc))
    last_seen = mapped_column(DateTime, nullable=True)
    version = mapped_column(String(32), nullable=True)
    enabled = mapped_column(Boolean, nullable=False, default=True)
    extra_config = mapped_column(MutableDict.as_mutable(JSON), default=dict)
    
    def __init__(self, **kwargs):
        self.modules = {}
        self._last_update_time = time.time()
        self.required_modules = []
        self.running = True
        self.load_modules()
        super().__init__(**kwargs)
        
    def load_modules(self):
        for _, module_name, _ in pkgutil.iter_modules(device_modules.__path__):
            module = importlib.import_module(f"{device_modules.__name__}.{module_name}")

            if hasattr(module, "register"):
                module_id, module = module.register(self)
                
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
            if hasattr(module, "preload"):
                module.preload()

        for module_id, module in self.modules.items():
            if hasattr(module, "start"):
                module.start()
                
        for module_id, module in self.modules.items():
            if hasattr(module, "post_start"):
                module.post_start()
                
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
            
    def shutdown(self):
        self.running = False
        
    def main_loop(self):
        while self.running:
            #print("src Loop Tick")
            self.update_modules()
            time.sleep(0.01) ## Allows other threads to run if they are implmented
            
        self.shutdown_modules()
        exit(0)