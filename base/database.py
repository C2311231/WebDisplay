from flask_sqlalchemy import SQLAlchemy
import uuid, json
from sqlalchemy.orm import Mapped, mapped_column
from base import commons
from flask import Flask
db = SQLAlchemy()


class Database(commons.BaseClass):
    def __init__(self, app: Flask, filepath: str="./db.db"):
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{filepath}"
        db.init_app(app)
        self.app = app

        with app.app_context():
            db.create_all()
        self.verify_config()

    def config(self) -> dict:
        with self.app.app_context():
            data_dict = {row.parameter: row.value for row in Config.query.all()}
            return data_dict

    def write_config(self, parameter: str, value: str) -> None:
        with self.app.app_context():
            config = self.config()
            if parameter in config.keys():
                    setting = Config.query.filter_by(parameter=parameter).first()
                    setting.value = value
                    db.session.commit()
            else:
                data = Config(parameter=parameter, value=value)
                db.session.add(data)
                db.session.commit()

    def verify_config(self) -> None:
        config = self.config()
        for key in self.required_config().keys():
            if key not in config.keys():
                value = self.required_config()[key]
                self.write_config(key, value)

    def write_event(
        self, name: str, color: str, wk_day: str, start_time: float, end_time: float, type: str, data: dict, sync_id: str | None=None
    ) -> None:
        if sync_id == None:
            sync_id = str(uuid.uuid4())
        
        with self.app.app_context():
            data = Events(
                name=name,
                color=color,
                wk_day=wk_day,
                start_time=start_time,
                end_time=end_time,
                type=type,
                data=json.dumps(data),
                sync_id=sync_id,
            )
            db.session.add(data)
            db.session.commit()
            id = data.id
            return id

    def edit_event(
        self, id: str, name: str, color: str, wk_day: str, start_time: float, end_time: float, type: str, data: dict, sync_id: str | None=None
    ) -> None:
        with self.app.app_context():
            if sync_id:
                event = Events.query.filter_by(sync_id=sync_id).first()
                event.name = name
                event.color = color
                event.wk_day = wk_day
                event.start_time = start_time
                event.end_time = end_time
                event.type = type
                event.data = json.dumps(data)
                db.session.commit()
                return event
            else:
                event = Events.query.filter_by(id=id).first()
                event.name = name
                event.color = color
                event.wk_day = wk_day
                event.start_time = start_time
                event.end_time = end_time
                event.type = type
                event.data = json.dumps(data)
                db.session.commit()
                return event

    def get_event(self, id: int) -> object:
        with self.app.app_context():
            data = Events.query.filter_by(id=id).first()
            return data

    def get_events(self) -> list[dict]:
        with self.app.app_context():
            data_dict = [row.__dict__ for row in Events.query.all()]
            for row in data_dict:
                row.pop("_sa_instance_state", None)
            return data_dict

    def delete_event(self, id: int) -> None:
        with self.app.app_context():
            event = Events.query.filter_by(id=id).first()
            db.session.delete(event)
            db.session.commit()

    def delete_sync_event(self, id: str) -> None:
        with self.app.app_context():
            event = Events.query.filter_by(syncID=id).first()
            db.session.delete(event)
            db.session.commit()

    def create_peer(
        self,
        web_version: str,
        api_version: str,
        web_url: str,
        web_port: int,
        web_encryption: bool,
        device_name: str,
        device_state: str,
        device_platform: str,
        device_id: str,
        device_ip: str,
        disabled: bool,
    ) -> int:
        with self.app.app_context():
            data = Peers(
                web_version=web_version,
                api_version=api_version,
                web_url=web_url,
                web_port=web_port,
                web_encryption=web_encryption,
                device_name=device_name,
                device_state=device_state,
                device_platform=device_platform,
                device_id=device_id,
                device_ip=device_ip,
                disabled=disabled,
            )
            db.session.add(data)
            db.session.commit()
            id = data.id
            return id

    def get_peer(self, id: int) -> dict:
        with self.app.app_context():
            data = Peers.query.filter_by(id=id).first()
            return data

    def get_peers(self) -> list[dict]:
        with self.app.app_context():
            data_dict = [row.__dict__ for row in Peers.query.all()]
            for row in data_dict:
                row.pop("_sa_instance_state", None)
            return data_dict

    def edit_peer(
        self,
        id,
        web_version: str = None,
        api_version: str = None,
        web_url: str = None,
        web_port: int = None,
        web_encryption: bool = None,
        device_name: str = None,
        device_state: str = None,
        device_platform: str = None,
        device_id: str = None,
        device_ip: str = None,
        disabled: bool = None,
    ) -> None:
        with self.app.app_context():
            peer = Peers.query.filter_by(id=id).first()
            
            if web_version != None:
                peer.web_version = web_version

            if api_version != None:
                peer.api_version = api_version

            if web_url != None:
                peer.web_url = web_url

            if web_encryption != None:
                peer.web_encryption = web_encryption

            if device_name != None:
                peer.device_name = device_name

            if device_state != None:
                peer.web_version = device_state

            if device_ip != None:
                peer.device_ip = device_ip

            if device_platform != None:
                peer.device_platform = device_platform

            if device_id != None:
                peer.device_id = device_id

            if web_port != None:
                peer.web_port = web_port

            if disabled != None:
                peer.disabled = disabled
                
            db.session.commit()

    def required_config() -> dict:
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


class Config(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    parameter: Mapped[str] = mapped_column(unique=True)
    value: Mapped[str]


class Events(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    color: Mapped[str]
    wk_day: Mapped[str]
    start_time: Mapped[float]
    end_time: Mapped[float]
    type: Mapped[str]
    sync_id: Mapped[str] = mapped_column(unique=True)
    data: Mapped[str]


class Peers(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    web_version: Mapped[str]
    api_version: Mapped[str]
    web_url: Mapped[str]
    web_port: Mapped[str]
    web_encryption: Mapped[str]
    device_name: Mapped[str]
    device_state: Mapped[str]
    device_platform: Mapped[str]
    device_id: Mapped[str] = mapped_column(unique=True)
    device_ip: Mapped[str]
    disabled: Mapped[bool]
