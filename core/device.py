from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from core.system_modules.database.extentions import db # TODO Find a way to validate this module exists (Or just make a system requried module handler)

class Device(db.Model):
    __tablename__ = "device"
    device_type = db.Column(db.String(20))  # discriminator
    
    __mapper_args__ = {
        "polymorphic_on": device_type,
        "polymorphic_identity": "device",
    }