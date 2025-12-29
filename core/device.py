from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()

class Device(db.Model):
    __tablename__ = "device"
    device_type = db.Column(db.String(20))  # discriminator
    
    __mapper_args__ = {
        "polymorphic_on": device_type,
        "polymorphic_identity": "device",
    }