from flask import render_template, redirect, Flask
from base import networking, database, browser, api, peers, cec, scheduler, calander
import sys
import socket

browser_manager = browser.BrowserManager()
app = Flask(__name__)
db = database.Database(app=app, filepath=sys.argv[1])
network_manager = networking.NetworkingManager(db)
cec_manager = cec.CecManager()
peer_manager = peers.PeerManager(network_manager, db=db)
calander_manager = calander.CalenderManager(db)
scheduler = scheduler.Scheduler(db, browser_manager, cec_manager)
peer_manager.start_discovery()
ip = network_manager.get_local_ip()
db.write_config("ip", ip)
db.write_config("url", f"http://{ip}:{sys.argv[2]}")
db.write_config("port", sys.argv[2])

# Testing Calander
calander_manager.add_calender("Test", "https://calendar.google.com/calendar/ical/c_5698af4cee1cc5fb5e42fba501a9a328425d63309ed4d781d6044ab5e8696a94%40group.calendar.google.com/public/basic.ics")


@app.route("/")
def home():
    return render_template(
        "index.html",
        peers=peer_manager.devices,
        title=db.config()["name"],
        name=db.config()["name"],
        config=db.config(),
        adapters=network_manager.get_interfaces(),
    )


@app.route("/idle/")
def idle_screen():
    return render_template(
        "idle.html", name=db.config()["name"], url=db.config()["url"]
    )

@app.route("/calender/")
def calender_screen():
    return render_template(
        "calender.html"
    )

@app.route("/getScreenshot/")
def screenshot():
    browser_manager.get_screenshot()
    return redirect("/static/images/latestScreenShot.png")


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


if __name__ == "__main__":
    scheduler.start()
    api_blueprint = api.api_v1(db, cec_manager, browser_manager, peer_manager, calander_manager).get_blueprint()
    app.register_blueprint(api_blueprint, url_prefix="/api")
    app.run(host="0.0.0.0", port=sys.argv[2], debug=False)
    scheduler.stop()
