from flask import render_template, Flask, request
from base import networking, database, browser, web_v2, peers, cec, scheduler, api_v2
import sys
import socket
local_config = {}

app = Flask(__name__)
db = database.Database(local_config, app=app, filepath=sys.argv[1])
browser_manager = browser.BrowserManager(local_config)
network_manager = networking.NetworkingManager(local_config, db)
cec_manager = cec.CecManager(local_config)
peer_manager = peers.PeerManager(local_config, network_manager, db=db)
api = api_v2.APIv2(local_config, db)
scheduler = scheduler.Scheduler(local_config, db, browser_manager, cec_manager)
peer_manager.start_discovery()
ip = network_manager.get_local_ip()
db.write_local_config("ip", ip)
db.write_local_config("url", f"http://{ip}:{sys.argv[2]}")
db.write_local_config("port", sys.argv[2])

@app.route("/api/", methods=["POST"])
def api_http_endpoint():
    """
    API HTTP endpoint for processing requests.
    (Just for reference, not finished implementing yet)
    """
    api_response = api.process_request(request.data.decode("utf-8"))
    return api_response.to_json(), api_response.code # type: ignore
    
@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    (Fixes a caching issue)
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


if __name__ == "__main__":
    scheduler.start()
    web_v2_blueprint = web_v2.get_blueprint()
    app.register_blueprint(web_v2_blueprint, url_prefix="/")
    app.run(host="0.0.0.0", port=int(sys.argv[2]), debug=False)
    scheduler.stop()
