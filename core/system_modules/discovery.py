"""
Discovery Module Manager

Part of WebDisplay
System Discovery Module

License: MIT license

Author: C2311231

Notes:
"""

import core.system_modules.database.database as database
import core.system_modules.api.api_v2 as api_v2
import core.system
import core.system_modules.database.settings_manager as settings_manager
import core.module as module

# TODO Reimplement Discovery Module
class DiscoveryManager(module.module):
    def __init__(self, system: core.system.system):
        self.system = system
        system.require_modules("settings_manager", "networking")
    
    def start(self) -> None:
        self.settings_manager: settings_manager.SettingsManager = self.system.get_module("settings_manager") # type: ignore
        #self.discover_engine = multicast_api_endpoint.DiscoveryEngine(config, db)
        self.networking = self.system.get_module("networking")
#        threading.Thread(target=self.check_device_connections, daemon=True).start()

    # def start_discovery(self) -> None:
    #     pass
    #     # threading.Thread(target=self.discover_engine.send_discovery, daemon=True).start()
    #     # threading.Thread(
    #     #     target=self.discover_engine.listen_for_discovery,
    #     #     daemon=True,
    #     #     args=(self.found_device,),
    #     # ).start()

    # def found_device(self, device_id:str, device_ip: str, device_port: int) -> None:
    #     peer = self.db.get_peer(device_id)
    #     if peer:
    #         peer.update_ip(device_ip)
    #         peer.device_port = device_port
    #         self.db.db.session.commit()
    #     else:
    #         self.add_device(commons.Address(device_ip), device_id, device_port)
        
    # def add_device(self, ip: commons.Address, device_id: str, port: int) -> None:
    #     device_name = api_v2.call_http_api(self.config["device_id"], str(ip), port, "get", device_id, "database", "get_config_entry", {"parameter": "device_name"})
    #     device_groups = api_v2.call_http_api(self.config["device_id"], str(ip), port, "get", device_id, "database", "get_config_entry", {"parameter": "device_groups"})
    #     if device_name.error == False and device_groups.error == False:
    #         self.db.write_peer(device_name=device_name.data["value"], device_id=device_id, device_ip=str(ip), groups=device_groups.data["value"])

    # def check_device_connections(self) -> None:
    #     while True:
    #         for device in self.db.get_peers():
    #             device.ping(self.config["device_id"])

    #         time.sleep(5)
            
    ## TODO Move all networking related config requirements to source from networking module

def register(system_manager):
    return "discovery", DiscoveryManager(system_manager)