from flask_sqlalchemy import SQLAlchemy
import uuid, json
from sqlalchemy.orm import Mapped, mapped_column
import commons
required_tables = {
        "config": {
                'parameter': 'TEXT NOT NULL',
                'value': 'TEXT NOT NULL'
            },
        "events": {
                'name': 'TEXT NOT NULL',
                'color': 'TEXT NOT NULL',
                'wkDay': 'TEXT NOT NULL',
                'startTime': 'TEXT NOT NULL',
                'endTime': 'TEXT NOT NULL',
                'type': 'TEXT NOT NULL',
                'data': 'TEXT NOT NULL'
            }
    }

required_config = {
    "id": str(uuid.uuid4()),
    "web_version": "1.0",
    "api_version": "1.0",
    "url": "http://localhost:5000",
    "port": "5000",
    "encription": "False",
    "name": "Screen One",
    "state": "online",
    "platform": "linux",
    "ip": "localhost"
}
db = SQLAlchemy()

class Database(commons.BaseClass):
    def __init__(self, app, filepath="./db.db"):
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{filepath}"
        db.init_app(app)
        self.app = app
        
        with app.app_context():
            db.create_all()
        self.verifyConfig()
    def config(self):
        with self.app.app_context():
            # data =  db.session.execute(db.select(Config)).scalars().all()
            data_dict = {row.parameter: row.value for row in Config.query.all()}
            return data_dict

    def writeConfig(self, parameter, value):
        with self.app.app_context():
            data = Config(
                parameter=parameter,
                value=value
            )
            db.session.add(data)
            db.session.commit()

    def verifyConfig(self):
        config = self.config()
        for key in required_config.keys():
            if key not in config.keys():
                value = required_config[key]
                self.writeConfig(key, value)
                
    def writeEvent(self, name, color, wkDay, startTime, endTime, type, data, syncID=None):
        if syncID == None:
            syncID = str(uuid.uuid4())
        with self.app.app_context():
            data = Events(name=name, color=color, wkDay=wkDay, startTime=startTime, endTime=endTime, type=type, data=json.dumps(data), syncID=syncID)
            db.session.add(data)
            db.session.commit()
            id = data.id
            return id
            
    def editEvent(self, id, name, color, wkDay, startTime, endTime, type, data, syncID=None):
        with self.app.app_context():
            if syncID:
                event = Events.query.filter_by(syncID=syncID).first()
                event.name = name
                event.color = color
                event.wkDay = wkDay
                event.startTime = startTime
                event.endTime = endTime
                event.type = type
                event.data = json.dumps(data)
                db.session.commit()
                return event
            else:
                event = Events.query.filter_by(id=id).first()
                event.name = name
                event.color = color
                event.wkDay = wkDay
                event.startTime = startTime
                event.endTime = endTime
                event.type = type
                event.data = json.dumps(data)
                db.session.commit()
                return event
            
    def getEvent(self, id):
        with self.app.app_context():
            
            data_dict = Events.query.filter_by(id=id).first()
            return data_dict
        
    def getEvents(self):
        with self.app.app_context():
            
            data_dict = [row.__dict__ for row in Events.query.all()]
            for row in data_dict:
                row.pop("_sa_instance_state", None)
            return data_dict
    
    def deleteEvent(self, id):
        with self.app.app_context():
            event = Events.query.filter_by(id=id).first()
            db.session.delete(event)
            db.session.commit()
            
    def deleteSyncEvent(self, id):
        with self.app.app_context():
            event = Events.query.filter_by(syncID=id).first()
            db.session.delete(event)
            db.session.commit()
            
    def createPeer(self, web_version, api_version, web_url, web_port, web_encription, device_name, device_state, device_platform, device_id, device_ip, disabled):
        with self.app.app_context():
            data = Peers(web_version=web_version, api_version=api_version, web_url=web_url, web_port=web_port, web_encription=web_encription, device_name=device_name, device_state=device_state, device_platform=device_platform, device_id=device_id, device_ip=device_ip, disabled=disabled)
            db.session.add(data)
            db.session.commit()
            id = data.id
            return id
    def getPeer(self, id):
        with self.app.app_context():
            
            data_dict = Peers.query.filter_by(id=id).first()
            return data_dict
        
    def getPeers(self):
        with self.app.app_context():
            
            data_dict = [row.__dict__ for row in Peers.query.all()]
            for row in data_dict:
                row.pop("_sa_instance_state", None)
            return data_dict
            
    def editPeer(self, id, web_version=None, api_version=None, web_url=None, web_port=None, web_encription=None, device_name=None, device_state=None, device_platform=None, device_id=None, device_ip=None, disabled=None):
        with self.app.app_context():
            peer = Peers.query.filter_by(id=id).first()
            if web_version != None:
                peer.web_version = web_version

            if api_version != None:
                peer.api_version = api_version
                
            if web_url != None:
                peer.web_url = web_url

            if web_encription != None:
                peer.web_encription = web_encription

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
class Config(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    parameter: Mapped[str] = mapped_column(unique=True)
    value: Mapped[str]

class Events(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    color: Mapped[str]
    wkDay: Mapped[str]
    startTime: Mapped[float]
    endTime: Mapped[float]
    type: Mapped[str]
    syncID: Mapped[str] = mapped_column(unique=True)
    data: Mapped[str]
    
class Peers(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    web_version: Mapped[str]
    api_version: Mapped[str]
    web_url: Mapped[str]
    web_port: Mapped[str]
    web_encription: Mapped[str]
    device_name: Mapped[str]
    device_state: Mapped[str]
    device_platform: Mapped[str]
    device_id: Mapped[str] = mapped_column(unique=True)
    device_ip: Mapped[str]
    disabled: Mapped[bool]
