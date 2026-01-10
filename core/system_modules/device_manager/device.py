from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import inspect
from core.system_modules.database.extentions import db # TODO Find a way to validate this module exists (Or just make a system requried module handler)
from sqlalchemy.ext.mutable import MutableDict

class Device(db.Model):
    __tablename__ = "device"
    

    
    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    device_type: Mapped[str] = mapped_column(db.String(20), nullable=False)  # discriminator
    device_name: Mapped[str] = mapped_column(nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, nullable=True)
    version = db.Column(db.String(32), nullable=True)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    extra_config = db.Column(MutableDict.as_mutable(db.JSON), default=dict)
    
    
    __mapper_args__ = {
        "polymorphic_on": device_type,
        "polymorphic_identity": "device",
    }

    def register_system(self, system) -> None:
        self.system = system
        
    def load_modules(self) -> None:
        pass
    
    