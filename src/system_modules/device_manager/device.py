"""
Device Module Device Base Class

Part of WebDisplay
System device_manager Module

License: MIT license

Author: C2311231

Notes:
"""

from datetime import datetime
from sqlalchemy import String, Integer, JSON, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from src.system_modules.database.extentions import db # TODO Find a way to validate this module exists (Or just make a system requried module handler)
from sqlalchemy.ext.mutable import MutableDict

class Device(db):
    __tablename__ = "device"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    device_type: Mapped[str] = mapped_column(String(20), nullable=False)  # discriminator
    device_name: Mapped[str] = mapped_column(nullable=False)
    created_at = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    last_seen = mapped_column(DateTime, nullable=True)
    version = mapped_column(String(32), nullable=True)
    enabled = mapped_column(Boolean, nullable=False, default=True)
    extra_config = mapped_column(MutableDict.as_mutable(JSON), default=dict)
    
    
    __mapper_args__ = {
        "polymorphic_on": device_type,
        "polymorphic_identity": "device",
    }

    def register_system(self, system) -> None:
        self.system = system
        
    def load_modules(self) -> None:
        pass
    
    