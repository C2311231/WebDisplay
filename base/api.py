from flask import Blueprint, redirect, request, make_response, jsonify
import json
import copy
from datetime import datetime
from base import commons, peers, browser, cec, database, updater, calander
import os, sys
from subprocess import call

DAYSOFWEEK = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]
EVENTTYPES = ["idle", "publishedSlide", "URL", "viewingSlide"]


class api_v1(commons.BaseClass):
    def __init__(
        self,
        database: database.Database,
        cec: cec.CecManager,
        browser_manager: browser.BrowserManager,
        peer_manager: peers.PeerManager,
        calender_manager: calander.CalenderManager
    ) -> None:
        self.cec = cec
        self.database = database
        self.browser = browser_manager
        self.peer_manager = peer_manager
        self.calendar_manager = calender_manager
        self.bp = Blueprint("api", __name__)
        self.register_routes()

    def register_routes(self):
        @self.bp.route("/status/")
        def api_request():
            init_message = {
                "web_version": self.database.config()["web_version"],
                "api_version": self.database.config()["api_version"],
                "web_url": self.database.config()["url"],
                "web_port": self.database.config()["port"],
                "web_encryption": self.database.config()["encryption"],
                "device_name": self.database.config()["name"],
                "device_state": self.database.config()["state"],
                "device_platform": self.database.config()["platform"],
                "device_id": self.database.config()["id"],
                "device_ip": self.database.config()["ip"],
            }
            return json.dumps(init_message, indent=4)

        @self.bp.route("/CEC/on/")
        def api_cec_on():
            self.cec.tv_on()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/off/")
        def api_cec_off():
            self.cec.tv_off()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/setActive/")
        def api_cec_Active():
            self.cec.set_active()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/volume/up/")
        def api_cec_volume_up():
            self.cec.volume_up()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/volume/down/")
        def api_cec_volume_down():
            self.cec.volume_down()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/volume/mute/")
        def api_cec_volume_mute():
            self.cec.toggle_mute()
            return make_response(json.dumps({}), 200)

        @self.bp.route("/CEC/get/power/")
        def api_cec_get_power():
            return make_response(json.dumps({"power": self.cec.get_tv_power()}), 200)

        @self.bp.route("/CEC/get/vender/")
        def api_cec_get_vender():
            return make_response(json.dumps({"vender": self.cec.get_vender()}), 200)

        @self.bp.route("/set/config/", methods=["POST"])
        def api_set_config():
            if request.is_json:
                print(request.json)
                self.database.write_config("name", str(request.json["name"]))
                self.database.write_config("reload_time", str(request.json["reload_time"]))
                data = {"message": "Success", "code": "Config Updated"}
                return make_response(jsonify(data), 200)
            data = {"message": "Failed", "code": "Request must be json"}
            return make_response(jsonify(data), 400)

        @self.bp.route("/add/peer/", methods=["POST"])
        def api_add_peer():
            self.peer_manager.add_device(request.json["ip"], request.json["port"])
            data = {"message": "Success", "code": "Peer Disabled"}
            return make_response(jsonify(data), 200)

        @self.bp.route("/disable/peer/<id>")
        def api_disable_peer(id: str):
            for peer in self.peer_manager.devices:
                if peer.device_id == id:
                    peer.disable()
                    data = {"message": "Success", "code": "Peer Disabled"}
                    return make_response(jsonify(data), 200)
            data = {"message": "Failed", "code": "Peer not found"}
            return make_response(jsonify(data), 400)

        @self.bp.route("/enable/peer/<id>")
        def api_enable_peer(id: str):
            for peer in self.peer_manager.devices:
                if peer.device_id == id:
                    peer.enable()
                    data = {"message": "Success", "code": "Peer Enabled"}
                    return make_response(jsonify(data), 200)
            data = {"message": "Failed", "code": "Peer not found"}
            return make_response(jsonify(data), 400)

        @self.bp.route("/add/schedule/event/", methods=["POST"])
        def api_add_schedule_event():

            if request.is_json:
                ## Data Validation
                if float(request.json["startTime"]) > float(request.json["endTime"]):
                    data = {
                        "message": "Failed",
                        "code": "End Time must come after Start Time.",
                    }
                    return make_response(jsonify(data), 400)

                if request.json["wkDay"] not in DAYSOFWEEK:
                    data = {
                        "message": "Failed",
                        "code": "Weekday must be one of: " + str(DAYSOFWEEK),
                    }
                    return make_response(jsonify(data), 400)

                if request.json["type"] not in EVENTTYPES:
                    data = {
                        "message": "Failed",
                        "code": "Type must be one of: " + str(EVENTTYPES),
                    }
                    return make_response(jsonify(data), 400)

                if self.database.get_event(request.json["id"]) == None:
                    if "syncID" in request.json.keys():
                        self.database.write_event(
                            request.json["name"],
                            request.json["color"],
                            request.json["wkDay"],
                            request.json["startTime"],
                            request.json["endTime"],
                            request.json["type"],
                            request.json["data"],
                            request.json["syncID"],
                        )
                    else:
                        id = self.database.write_event(
                            request.json["name"],
                            request.json["color"],
                            request.json["wkDay"],
                            request.json["startTime"],
                            request.json["endTime"],
                            request.json["type"],
                            request.json["data"],
                        )
                        peers = request.json["data"]["peers"]
                        print(f"created event: {id}")
                        event = self.database.get_event(id)
                        for peer in self.peer_manager.devices:
                            if peer.device_id in peers and not peer.disabled:
                                peer.sync_event(
                                    copy.deepcopy(event), self.database.config()["id"]
                                )

                else:
                    if "syncID" in request.json.keys():
                        self.database.edit_event(
                            request.json["id"],
                            request.json["name"],
                            request.json["color"],
                            request.json["wkDay"],
                            request.json["startTime"],
                            request.json["endTime"],
                            request.json["type"],
                            request.json["data"],
                            request.json["syncID"],
                        )
                    else:
                        original_event = self.database.get_event(request.json["id"])
                        event = self.database.edit_event(
                            request.json["id"],
                            request.json["name"],
                            request.json["color"],
                            request.json["wkDay"],
                            request.json["startTime"],
                            request.json["endTime"],
                            request.json["type"],
                            request.json["data"],
                        )
                        peers = request.json["data"]["peers"]
                        event = self.database.get_event(request.json["id"])
                        for peer in self.peer_manager.devices:
                            if (
                                peer.device_id
                                in json.loads(original_event.data)["peers"]
                                and peer.device_id not in peers
                                and not peer.disabled
                            ):
                                peer.delete_event(event.sync_id)
                            elif (
                                peer.device_id
                                not in json.loads(original_event.data)["peers"]
                                and peer.device_id in peers
                                and not peer.disabled
                            ):
                                temp_event = copy.deepcopy(event)
                                temp_event.id = "0"
                                peer.sync_event(
                                    temp_event, self.database.config()["id"]
                                )

                            elif peer.device_id in peers and not peer.disabled:
                                peer.sync_event(
                                    copy.deepcopy(event), self.database.config()["id"]
                                )

                    t = (
                        float(datetime.now().strftime("%H"))
                        + float(datetime.now().strftime("%M")) / 60
                    )

                    wk_day = datetime.now().strftime("%A")
                    if request.json["wkDay"] == wk_day:
                        if (float(request.json["startTime"]) <= t) and (
                            float(request.json["endTime"]) > t
                        ):
                            self.browser.set_event(0)
                data = {"message": "Done", "code": "SUCCESS"}
                return make_response(jsonify(data), 200)
            return make_response({}, 400)

        @self.bp.route("/remove/schedule/event/<id>")
        def api_remove_schedule_event(id: str):
            if id.isdigit():
                self.database.delete_event(id)
            else:
                self.database.delete_sync_event(id)
            data = {"message": "Done", "code": "SUCCESS"}
            return make_response(jsonify(data), 200)

        @self.bp.route("/get/can_schedule/event/", methods=["POST"])
        def api_can_schedule_event():
            pass

        @self.bp.route("/get/schedule/event/")
        def api_get_schedule_event():
            return make_response(json.dumps(self.database.get_events()), 200)
        
        @self.bp.route("/update/releaseNotes/")
        def get_release_notes():
            return make_response(json.dumps({"data": updater.fetch_release_notes_from_github()}), 200) 
        
        @self.bp.route("/update/available/")
        def get_update_available():
            return make_response(json.dumps({"update_available": updater.is_update_available()}), 200)
        
        @self.bp.route("/update/update/")
        def start_update():
            updater.main()
            print("Relaunching program...")
            python = sys.executable
            os.execv(python, [python] + sys.argv)
            
        @self.bp.route("/update/nextVersion/")
        def get_next_version():
            return make_response(json.dumps({"version": "testVersion"}), 200)
            
        @self.bp.route("/restart/")
        def restart():
            call("sudo reboot", shell=True)
            
        @self.bp.route("/get/calender_data/<id>")
        def get_cal_data(id):
            return make_response(json.dumps({"data": self.calendar_manager.get_calender_by_id(id).get_dict()}), 200)
        
        @self.bp.route("/get/calender_events/<id>/<day>/<month>/<year>")
        def get_cal_events(id, day: int, month: int, year: int):
            cal = self.calendar_manager.get_calender_by_id(id)
            events = cal.events_on(day, month, year)
            

    def get_blueprint(self):
        return self.bp
