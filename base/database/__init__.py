from flask_sqlalchemy import SQLAlchemy
import uuid, json
from base import commons
from flask import Flask
from .models import Config, Events, Peers, db, MetaData, GlobalConfig


class Database(commons.BaseClass):
    def __init__(self, config: dict, app: Flask, filepath: str="./db.db"):
        app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{filepath}"
        db.init_app(app)
        self.app = app
        self.db = db
        with app.app_context():
            db.create_all()
        self.config = config
                
    def write_local_config_if_not_exists(self, config: dict) -> None:
        """Write local configuration parameters if they do not already exist."""
        with self.app.app_context():
            local_device_id = config["device_id"] if not db.session.query(MetaData).filter_by(parameter="device_id").first() else db.session.query(MetaData).filter_by(parameter="device_id").first().value # type: ignore
            for parameter, value in config.items():
                existing_config = db.session.query(Config).filter_by(parameter=parameter, device=local_device_id).first()
                if not existing_config:
                    if parameter == "device_id":
                        id = MetaData(parameter="device_id", value=str(value))  # type: ignore
                        db.session.add(id)
                        db.session.commit()
                    new_config = Config(parameter=parameter, value=value, device=local_device_id) # type: ignore
                    db.session.add(new_config)
                    db.session.commit()
    
    def initialize_local_config(self) -> None:
        """Initialize local configuration parameters in the database."""
        self.config.update(self.get_device_config(self.get_device_id())) # type: ignore
    
    def get_device_id(self) -> str:
        """Get the device ID from the database."""
        with self.app.app_context():
            id = db.session.query(MetaData).filter_by(parameter="device_id").first()
            if id:
                return id.value
            raise Exception("Device ID not found in database. Please ensure the database is initialized correctly.")

    def get_config_entry(self, parameter: str, device_id: str) -> Config | None:
        """Get a specific configuration parameter for a specific device."""
        with self.app.app_context():
            return db.session.query(Config).filter_by(device=device_id, parameter=parameter).first()
            
    def write_local_config(self, parameter: str, value: str) -> None:
        """Write a local configuration parameter."""
        with self.app.app_context():
            config = db.session.query(Config).filter_by(parameter=parameter).first()
            if config:
                config.value = value
            else:
                new_config = Config(parameter=parameter, value=value, device=self.get_device_id())  # type: ignore
                db.session.add(new_config)
                db.session.commit()
                
            config = self.get_device_config(self.get_device_id())

    def get_device_config(self, device_id: str) -> dict:
        """Get the configuration of a specific device."""
        with self.app.app_context():
            config = db.session.query(Config).filter_by(device=device_id).all()
            return {c.parameter: c.value for c in config}
        
    def write_config(self, parameter: str, value: str, device_id: str) -> None:
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
                return event.to_dict()
            return {}
    
    def write_event(self, name: str, groups: list[str], criteria: str, action: str, color: str, priority: int, enabled: bool, startdate: str, enddate: str) -> None:
        """Write a new event to the database."""
        with self.app.app_context():
            new_event = Events(name=name, groups=groups, criteria=criteria, action=action, color=color, priority=priority, enabled=enabled, startdate=startdate, enddate=enddate) # type: ignore
            db.session.add(new_event)
            db.session.commit()
    
    def get_events(self) -> list[dict]:
        """Get all events from the database."""
        with self.app.app_context():
            events = db.session.query(Events).all()
            return [
                event.to_dict()
                for event in events
            ]
            
    def get_peer(self, device_id: str) -> Peers | None:
        """Get the details of a specific peer device."""
        with self.app.app_context():
            return db.session.query(Peers).filter_by(device_id=device_id).first()
            
        
    def write_peer(self, device_name: str, device_id: str, device_ip: str, groups: list[str]) -> None:
        """Write a new peer device to the database."""
        with self.app.app_context():
            new_peer = Peers(device_name=device_name, device_id=device_id, device_ip=device_ip, groups=groups) # type: ignore
            db.session.add(new_peer)
            db.session.commit()
    
    def get_peers(self) -> list[Peers]:
        """Get all peer devices from the database."""
        with self.app.app_context():
            peers = db.session.query(Peers).all()
            return peers
    def _api_get_events(self) -> commons.Response:
        """API endpoint to get all events."""
        try:
            events = self.get_events()
            return commons.Response(False, "success", "Events retrieved successfully", 200, {"events": events})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to retrieve events: {str(e)}", 500, {})
    
    def _api_get_peers(self) -> commons.Response:
        """API endpoint to get all peer devices."""
        try:
            peers = self.get_peers()
            return commons.Response(False, "success", "Peers retrieved successfully", 200, {"peers": [peer.to_dict() for peer in peers]})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to retrieve peers: {str(e)}", 500, {})
        
    def _api_get_config(self, device_id: str = "0") -> commons.Response:
        """API endpoint to get the configuration of a specific device."""
        try:
            config = self.get_device_config(device_id)
            return commons.Response(False, "success", "Configuration retrieved successfully", 200, {"config": config})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to retrieve configuration: {str(e)}", 500, {})
        
    def _api_get_event(self, event_id: str) -> commons.Response:
        """API endpoint to get the details of a specific event."""
        try:
            event = self.get_event(event_id)
            if event:
                return commons.Response(False, "success", "Event retrieved successfully", 200, {"event": event})
            else:
                return commons.Response(True, "error", "Event not found", 404, {})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to retrieve event: {str(e)}", 500, {})
        
    def _api_get_peer(self, device_id: str) -> commons.Response:
        """API endpoint to get the details of a specific peer device."""
        try:
            peer = self.get_peer(device_id)
            if peer:
                return commons.Response(False, "success", "Peer retrieved successfully", 200, {"peer": peer})
            else:
                return commons.Response(True, "error", "Peer not found", 404, {})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to retrieve peer: {str(e)}", 500, {})
        
    def _api_get_config_entry(self, parameter: str, device_id: str = "0") -> commons.Response:
        """API endpoint to get a specific configuration parameter for a specific device."""
        try:
            value = self.get_config_entry(parameter, device_id)
            if value:
                return commons.Response(False, "success", "Configuration entry retrieved successfully", 200, {"value": value.to_dict()})
            else:
                return commons.Response(True, "error", "Configuration entry not found", 404, {})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to retrieve configuration entry: {str(e)}", 500, {})
        
    def _api_get_config_check_data(self) -> commons.Response:
        """API endpoint to get the check data for the configuration."""
        try:
            config = Config.query.all()
            check_data = [c.check_data for c in config]
            return commons.Response(False, "success", "Configuration check data retrieved successfully", 200, {"check_data": check_data})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to retrieve configuration check data: {str(e)}", 500, {})
        
    def _api_get_peers_check_data(self) -> commons.Response:
        """API endpoint to get the check data for the peers."""
        try:
            peers = Peers.query.all()
            peers = {c.parameter: c.check_data for c in peers}
            check_data = {key: value for key, value in peers.items() if key == "check_data"}
            return commons.Response(False, "success", "Peers check data retrieved successfully", 200, {"check_data": check_data})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to retrieve peers check data: {str(e)}", 500, {})
    
    def _api_get_events_check_data(self) -> commons.Response:
        """API endpoint to get the check data for the events."""
        try:
            events = Events.query.all()
            events = {c.parameter: c.check_data for c in events}
            check_data = {key: value for key, value in events.items() if key == "check_data"}
            return commons.Response(False, "success", "Events check data retrieved successfully", 200, {"check_data": check_data})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to retrieve events check data: {str(e)}", 500, {})
        
    def _api_set_config(self, parameter: str, value: str, device_id: str = "0") -> commons.Response:
        """API endpoint to set a configuration parameter for a specific device."""
        try:
            self.write_config(parameter, value, device_id)
            return commons.Response(False, "success", "Configuration updated successfully", 200, {})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to update configuration: {str(e)}", 500, {})
        
    def _api_set_event(self, name: str, groups: list[str], criteria: str, action: str, color: str, priority: int, enabled: bool, startdate: str, enddate: str) -> commons.Response:
        """API endpoint to set a new event."""
        try:
            self.write_event(name, groups, criteria, action, color, priority, enabled, startdate, enddate)
            return commons.Response(False, "success", "Event created successfully", 200, {})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to create event: {str(e)}", 500, {})
        
    def _api_set_peer(self, device_name: str, device_id: str, device_ip: str, groups: list[str]) -> commons.Response:
        """API endpoint to set a new peer device."""
        try:
            self.write_peer(device_name, device_id, device_ip, groups)
            return commons.Response(False, "success", "Peer created successfully", 200, {})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to create peer: {str(e)}", 500, {})
        
    def _api_delete_event(self, event_id: str) -> commons.Response:
        """API endpoint to delete a specific event."""
        try:
            with self.app.app_context():
                event = db.session.query(Events).filter_by(id=event_id).first()
                if event:
                    db.session.delete(event)
                    db.session.commit()
                    return commons.Response(False, "success", "Event deleted successfully", 200, {})
                else:
                    return commons.Response(True, "error", "Event not found", 404, {})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to delete event: {str(e)}", 500, {})
        
    def _api_delete_peer(self, device_id: str) -> commons.Response:
        """API endpoint to delete a specific peer device."""
        try:
            with self.app.app_context():
                peer = db.session.query(Peers).filter_by(device_id=device_id).first()
                if peer:
                    db.session.delete(peer)
                    db.session.commit()
                    return commons.Response(False, "success", "Peer deleted successfully", 200, {})
                else:
                    return commons.Response(True, "error", "Peer not found", 404, {})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to delete peer: {str(e)}", 500, {})
        
    def _api_delete_config_entry(self, parameter: str, device_id: str = "0") -> commons.Response:
        """API endpoint to delete a specific configuration parameter for a specific device."""
        try:
            with self.app.app_context():
                config = db.session.query(Config).filter_by(device=device_id, parameter=parameter).first()
                if config:
                    db.session.delete(config)
                    db.session.commit()
                    return commons.Response(False, "success", "Configuration entry deleted successfully", 200, {})
                else:
                    return commons.Response(True, "error", "Configuration entry not found", 404, {})
        except Exception as e:
            return commons.Response(True, "error", f"Failed to delete configuration entry: {str(e)}", 500, {})
        
        
    def required_config(self) -> dict:
        # Required configuration data in database in format {parameter: default} (None results in defaulting to parameters set by other classes, if none are set an error will be thrown)
        data = {
                "device_id": str(uuid.uuid4()),
                "web_version": "1.0",
                "api_version": "1.0",
                "url": "http://localhost:80",
                "port": "80",
                "encryption": "False",
                "name": "Screen One",
                "state": "online",
                "platform": "linux",
                "ip": "localhost",
                "reload_time": "0"
        }
        return data
    
    def tick(self) -> None:
        self.initialize_local_config() # update config dict each tick
    
    def api_endpoints(self) -> list[dict]:
        # API endpoints in format [{"endpoint_type": "endpoint_type", "function": function, "endpoint_domain": "domain", "endpoint_name": "name"}] (function must return a response object)
        return [
            {
                "endpoint_type": "get",
                "function": self._api_get_events,
                "endpoint_domain": "database",
                "endpoint_name": "events",
            },
            {
                "endpoint_type": "get",
                "function": self._api_get_peers,
                "endpoint_domain": "database",
                "endpoint_name": "peers",
            },
            {
                "endpoint_type": "get",
                "function": self._api_get_config,
                "endpoint_domain": "database",
                "endpoint_name": "config",
            },
            {
                "endpoint_type": "get",
                "function": self._api_get_event,
                "endpoint_domain": "database",
                "endpoint_name": "event",
            },
            {
                "endpoint_type": "get",
                "function": self._api_get_peer,
                "endpoint_domain": "database",
                "endpoint_name": "peer",
            },
            {
                "endpoint_type": "get",
                "function": self._api_get_config_entry,
                "endpoint_domain": "database",
                "endpoint_name": "config_entry",
            },
            {
                "endpoint_type": "get",
                "function": self._api_get_config_check_data,
                "endpoint_domain": "database",
                "endpoint_name": "config_check_data",
            },
            {
                "endpoint_type": "get",
                "function": self._api_get_peers_check_data,
                "endpoint_domain": "database",
                "endpoint_name": "peers_check_data",
            },
            {
                "endpoint_type": "get",
                "function": self._api_get_events_check_data,
                "endpoint_domain": "database",
                "endpoint_name": "events_check_data",
            },
            {
                "endpoint_type": "post",
                "function": self._api_set_config,
                "endpoint_domain": "database",
                "endpoint_name": "config_entry",
            },
            {
                "endpoint_type": "post",
                "function": self._api_set_event,
                "endpoint_domain": "database",
                "endpoint_name": "event",
            },
            {
                "endpoint_type": "post",
                "function": self._api_set_peer,
                "endpoint_domain": "database",
                "endpoint_name": "peer",
            },
            {
                "endpoint_type": "delete",
                "function": self._api_delete_event,
                "endpoint_domain": "database",
                "endpoint_name": "event",
            },
            {
                "endpoint_type": "delete",
                "function": self._api_delete_peer,
                "endpoint_domain": "database",
                "endpoint_name": "peer",
            },
            {
                "endpoint_type": "delete",
                "function": self._api_delete_config_entry,
                "endpoint_domain": "database",
                "endpoint_name": "config_entry",
            }
        ]