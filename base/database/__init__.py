from flask_sqlalchemy import SQLAlchemy
import uuid, json
from base import commons
from flask import Flask
from .models import Config, Events, Peers, db


class Database(commons.BaseClass):
    def __init__(self, app: Flask, filepath: str="./db.db"):
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{filepath}"
        db.init_app(app)
        self.app = app

        with app.app_context():
            db.create_all()
        self.verify_config()

    def verify_config(self) -> None:
        config = self.get_device_config("0")
        for key in self.required_config().keys():
            if key not in config.keys():
                value = self.required_config()[key]
                self.write_config(key, value)

    def get_config_entry(self, parameter: str, device_id: str = "0") -> str:
        """Get a specific configuration parameter for a specific device."""
        with self.app.app_context():
            config = db.session.query(Config).filter_by(device=device_id, parameter=parameter).first()
            if config:
                return config.value
            return ""

    def get_device_config(self, device_id: str) -> dict:
        """Get the configuration of a specific device."""
        with self.app.app_context():
            config = db.session.query(Config).filter_by(device=device_id).all()
            return {c.parameter: c.value for c in config}
        
    def write_config(self, parameter: str, value: str, device_id: str = "0") -> None:
        """Write a configuration parameter for a specific device."""
        with self.app.app_context():
            config = db.session.query(Config).filter_by(device=device_id, parameter=parameter).first()
            if config:
                config.value = value
            else:
                new_config = Config(device=device_id, parameter=parameter, value=value) # type: ignore
                db.session.add(new_config)
            db.session.commit()
            
    def get_event(self, event_id: str) -> dict:
        """Get the details of a specific event."""
        with self.app.app_context():
            event = db.session.query(Events).filter_by(id=event_id).first()
            if event:
                return {
                    "id": event.id,
                    "name": event.name,
                    "groups": event.groups,
                    "criteria": event.criteria,
                    "action": event.action,
                    "color": event.color,
                    "lastchanged": event.lastchanged.isoformat(),
                    "check_data": event.check_data
                }
            return {}
    
    def write_event(self, name: str, groups: list[str], criteria: str, action: str, color: str) -> None:
        """Write a new event to the database."""
        with self.app.app_context():
            new_event = Events(name=name, groups=groups, criteria=criteria, action=action, color=color) # type: ignore
            db.session.add(new_event)
            db.session.commit()
    
    def get_events(self) -> list[dict]:
        """Get all events from the database."""
        with self.app.app_context():
            events = db.session.query(Events).all()
            return [
                {
                    "id": event.id,
                    "name": event.name,
                    "groups": event.groups,
                    "criteria": event.criteria,
                    "action": event.action,
                    "color": event.color,
                    "lastchanged": event.lastchanged.isoformat(),
                    "check_data": event.check_data
                }
                for event in events
            ]
            
    def get_peer(self, device_id: str) -> dict:
        """Get the details of a specific peer device."""
        with self.app.app_context():
            peer = db.session.query(Peers).filter_by(device_id=device_id).first()
            if peer:
                return {
                    "id": peer.id,
                    "device_name": peer.device_name,
                    "device_id": peer.device_id,
                    "device_ip": peer.device_ip,
                    "groups": peer.groups,
                    "lastchanged": peer.lastchanged.isoformat(),
                    "check_data": peer.check_data
                }
            return {}
        
    def write_peer(self, device_name: str, device_id: str, device_ip: str, groups: list[str]) -> None:
        """Write a new peer device to the database."""
        with self.app.app_context():
            new_peer = Peers(device_name=device_name, device_id=device_id, device_ip=device_ip, groups=groups) # type: ignore
            db.session.add(new_peer)
            db.session.commit()
    
    def get_peers(self) -> list[dict]:
        """Get all peer devices from the database."""
        with self.app.app_context():
            peers = db.session.query(Peers).all()
            return [
                {
                    "id": peer.id,
                    "device_name": peer.device_name,
                    "device_id": peer.device_id,
                    "device_ip": peer.device_ip,
                    "groups": peer.groups,
                    "lastchanged": peer.lastchanged.isoformat(),
                    "check_data": peer.check_data
                }
                for peer in peers
            ]
    
    def required_config(self) -> dict:
        # Required configuration data in database in format {parameter: default} (None results in defaulting to parameters set by other classes, if none are set an error will be thrown)
        data = {
                "id": str(uuid.uuid4()),
                "web_version": "1.0",
                "api_version": "1.0",
                "url": "http://localhost:5000",
                "port": "5000",
                "encryption": "False",
                "name": "Screen One",
                "state": "online",
                "platform": "linux",
                "ip": "localhost",
                "reload_time": "0"
        }
        return data