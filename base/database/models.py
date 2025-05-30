from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
import datetime
import uuid
import requests
db = SQLAlchemy()


class Config(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    device: Mapped[list[str]]
    parameter: Mapped[str] = mapped_column(unique=True)
    value: Mapped[str]
    lastchanged: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    check_data: Mapped[str] = mapped_column(default=lambda: uuid.uuid4().hex, onupdate=lambda: uuid.uuid4().hex)
    
    def to_dict(self) -> dict:
        # Returns a dictionary representation of the config
        return {
            "id": self.id,
            "device": self.device,
            "parameter": self.parameter,
            "value": self.value,
            "lastchanged": self.lastchanged.isoformat() if self.lastchanged else None,
            "check_data": self.check_data,
        }

    def update_value(self, new_value: str):
        # Updates the value of the config parameter
        self.value = new_value

    def is_for_device(self, device_name: str) -> bool:
        # Checks if the config is associated with a specific device
        return device_name in self.device if self.device else False

class Events(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    groups: Mapped[list[str]]
    criteria: Mapped[str]
    action: Mapped[str]
    color: Mapped[str]
    lastchanged: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    check_data: Mapped[str] = mapped_column(default=lambda: uuid.uuid4().hex, onupdate=lambda: uuid.uuid4().hex)
    
    def to_dict(self) -> dict:
        # Returns a dictionary representation of the event
        return {
            "id": self.id,
            "name": self.name,
            "groups": self.groups,
            "criteria": self.criteria,
            "action": self.action,
            "color": self.color,
            "lastchanged": self.lastchanged.isoformat() if self.lastchanged else None,
            "check_data": self.check_data,
        }

    def is_in_group(self, group: str) -> bool:
        # Checks if the event is associated with a specific group
        return group in self.groups if self.groups else False


class Peers(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    device_name: Mapped[str]
    device_id: Mapped[str] = mapped_column(unique=True)
    device_ip: Mapped[str]
    groups: Mapped[list[str]]
    lastchanged: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.now(datetime.timezone.utc), onupdate=lambda: datetime.datetime.now(datetime.timezone.utc))
    check_data: Mapped[str] = mapped_column(default=lambda: uuid.uuid4().hex, onupdate=lambda: uuid.uuid4().hex)
    last_contact: Mapped[datetime.datetime] = mapped_column(default=lambda: datetime.datetime.min)

    def ping(self, source_id) -> bool:
        # This method is used to ping the peer device to check if it is online
        response = requests.post(
            f"http://{self.device_ip}/api/",
            json={
             "type": "trigger",
             "version": "v2",
             "destination": self.device_id,
             "source": source_id,
             "domain": "api",
             "name": "noOp",
             "data": {}
         }
        )
        
        response_data = response.json()
        return response.ok and response_data["status"] == "success"
    
    def to_dict(self) -> dict:
        # Returns a dictionary representation of the peer
        return {
            "id": self.id,
            "device_name": self.device_name,
            "device_id": self.device_id,
            "device_ip": self.device_ip,
            "groups": self.groups,
            "lastchanged": self.lastchanged.isoformat(),
            "check_data": self.check_data,
            "last_contact": self.last_contact.isoformat() if self.last_contact else None,
        }

    def update_ip(self, new_ip: str):
        # Updates the device IP address
        self.device_ip = new_ip

    def is_in_group(self, group: str) -> bool:
        # Checks if the peer belongs to a specific group
        return group in self.groups if self.groups else False