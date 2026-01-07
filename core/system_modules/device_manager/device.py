from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import inspect
from core.system_modules.database.extentions import db # TODO Find a way to validate this module exists (Or just make a system requried module handler)
from sqlalchemy.ext.mutable import MutableDict

class Device(db.Model):
    __tablename__ = "device"
    device_type = db.Column(db.String(20))  # discriminator

    config = db.Column(MutableDict.as_mutable(db.JSON), default=dict)

    
    __mapper_args__ = {
        "polymorphic_on": device_type,
        "polymorphic_identity": "device",
    }

    def register_system(self, system) -> None:
        self.system = system
        
    def load_modules(self) -> None:
        pass