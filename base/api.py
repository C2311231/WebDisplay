from flask import Blueprint, redirect, request, make_response, jsonify
import json
import copy
import commons
daysOfWeek = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
eventTypes = ["idle", "publishedSlide", "URL", "viewingSlide"]

class APIV1(commons.BaseClass):
    def __init__(self, database, cec, browserManager, peerManager):
        self.cec = cec
        self.database = database
        self.browser = browserManager
        self.peerManager = peerManager
        self.bp = Blueprint('api', __name__)
        self.register_routes()
        self.recivedMessageIDs = []

    def register_routes(self):
        @self.bp.route("/status/")
        def api_request():
            init_message = {
                "web_version": self.database.config()["web_version"],
                "api_version": self.database.config()["api_version"],
                "web_url": self.database.config()["url"],
                "web_port": self.database.config()["port"],
                "web_encription": self.database.config()["encription"],
                "device_name": self.database.config()["name"],
                "device_state": self.database.config()["state"],
                "device_platform": self.database.config()["platform"],
                "device_id": self.database.config()["id"],
                "device_ip": self.database.config()["ip"] 
            }
            return json.dumps(init_message, indent=4)

        @self.bp.route("/CEC/on/")
        def api_CEC_on():
            self.cec.tv_on()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/off/")
        def api_CEC_off():
            self.cec.tv_off()
            return make_response(json.dumps({}), 200)
        
        @self.bp.route("/CEC/setActive/")
        def api_CEC_Active():
            self.cec.set_active()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/volume/up/")
        def api_CEC_volume_up():
            self.cec.volume_up()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/volume/down/")
        def api_CEC_volume_down():
            self.cec.volume_down()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/volume/mute/")
        def api_CEC_volume_mute():
            self.cec.toggle_mute()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/get/power/")
        def api_CEC_get_power():
            return make_response(json.dumps({"power": self.cec.get_tv_power()}), 200)

        @self.bp.route("/CEC/get/vender/")
        def api_CEC_get_vender():
            return make_response(json.dumps({"vender": self.cec.get_vender()}), 200)

        @self.bp.route("/set/config/")
        def api_set_config():
            pass

        @self.bp.route("/add/peer/", methods=['POST'])
        def api_add_peer():
            self.peerManager.addDevice(request.json['ip'], request.json['port'])
            data = {'message': 'Sucsess', 'code': 'Peer Disabled'}
            return make_response(jsonify(data), 200)

        @self.bp.route("/disable/peer/<id>")
        def api_disable_peer(id):
            for peer in self.peerManager.devices:
                if peer.device_id == id:
                    peer.disable()
                    data = {'message': 'Sucsess', 'code': 'Peer Disabled'}
                    return make_response(jsonify(data), 200)
            data = {'message': 'Failed', 'code': 'Peer not found'}
            return make_response(jsonify(data), 400)
        
        @self.bp.route("/enable/peer/<id>")
        def api_enable_peer(id):
            for peer in self.peerManager.devices:
                if peer.device_id == id:
                    peer.enable()
                    data = {'message': 'Sucsess', 'code': 'Peer Enabled'}
                    return make_response(jsonify(data), 200)
            data = {'message': 'Failed', 'code': 'Peer not found'}
            return make_response(jsonify(data), 400)
        
        @self.bp.route("/add/schedule/event/", methods=['POST'])
        def api_add_schedule_event():
            
            if request.is_json:
                ## Data Validataion
                if float(request.json['startTime']) > float(request.json['endTime']):
                    data = {'message': 'Failed', 'code': 'End Time must come after Start Time.'}
                    return make_response(jsonify(data), 400)
                
                if request.json['wkDay'] not in daysOfWeek:
                    data = {'message': 'Failed', 'code': 'Weekday must be one of: ' + str(daysOfWeek)}
                    return make_response(jsonify(data), 400)
                
                if request.json['type'] not in eventTypes:
                    data = {'message': 'Failed', 'code': 'Type must be one of: ' + str(eventTypes)}
                    return make_response(jsonify(data), 400)
                
                if self.database.getEvent(request.json["id"]) == None:
                    if "syncID" in request.json.keys():
                        self.database.writeEvent(request.json['name'], request.json['color'], request.json['wkDay'], request.json['startTime'], request.json['endTime'], request.json['type'], request.json['data'], request.json["syncID"])
                    else:
                        id = self.database.writeEvent(request.json['name'], request.json['color'], request.json['wkDay'], request.json['startTime'], request.json['endTime'], request.json['type'], request.json['data'])
                        peers = request.json["data"]["peers"]
                        print(f"created event: {id}")
                        event = self.database.getEvent(id)
                        for peer in self.peerManager.devices and not peer.disabled:
                            if peer.device_id in peers:
                                peer.syncEvent(copy.deepcopy(event), self.database.config()["id"])
                
                else:
                    if "syncID" in request.json.keys():
                        self.database.editEvent(request.json["id"], request.json['name'], request.json['color'], request.json['wkDay'], request.json['startTime'], request.json['endTime'], request.json['type'], request.json['data'], request.json["syncID"])
                    else:
                        originalEvent = self.database.getEvent(request.json["id"])
                        event = self.database.editEvent(request.json["id"], request.json['name'], request.json['color'], request.json['wkDay'], request.json['startTime'], request.json['endTime'], request.json['type'], request.json['data'])
                        peers = request.json["data"]["peers"]
                        event = self.database.getEvent(request.json["id"])
                        for peer in self.peerManager.devices:
                            if peer.device_id in json.loads(originalEvent.data)["peers"] and peer.device_id not in peers and not peer.disabled:
                                peer.deleteEvent(event.syncID)
                                ## Must create new event on newly added peer if it doesn't yet exist and then must delete event from any peers that get removed from event sync
                                
                            elif peer.device_id not in json.loads(originalEvent.data)["peers"] and peer.device_id in peers and not peer.disabled:
                                tempEvent = copy.deepcopy(event)
                                tempEvent.id = "0"
                                peer.syncEvent(tempEvent, self.database.config()["id"])
                            
                            elif peer.device_id in peers and not peer.disabled:
                                peer.syncEvent(copy.deepcopy(event), self.database.config()["id"])
                        
                data = {'message': 'Done', 'code': 'SUCCESS'}
                return make_response(jsonify(data), 200)
            return make_response({}, 400)

        @self.bp.route("/remove/schedule/event/<id>")
        def api_remove_schedule_event(id):
            if id.isdigit():
                self.database.deleteEvent(id)            
            else:
                self.database.deleteSyncEvent(id)
            data = {'message': 'Done', 'code': 'SUCCESS'}
            return make_response(jsonify(data), 200)
            
        @self.bp.route("/get/can_schedule/event/", methods=['POST'])
        def api_can_schedule_event():
            pass

        @self.bp.route("/get/schedule/event/")
        def api_get_schedule_event():
            return make_response(json.dumps(self.database.getEvents()), 200)
        
    def get_blueprint(self):
        return self.bp