from flask import render_template, redirect, Flask
import time
from subprocess import call
import networking, database, browserManager, api, peerManager, cecManager, scheduler
from flask_sqlalchemy import SQLAlchemy
import sys
print("mainCall")
manager = browserManager.BrowserManager()
app = Flask(__name__)
db = database.Database(app=app, filepath=sys.argv[1])
networkManager = networking.NetworkingManager(db)
cecManag = cecManager.cecManager()
peerManag = peerManager.PeerManager(networkManager, db=db)
# initialize the app with the extension
scheduler = scheduler.scheduler(db, manager, cecManag)
peerManag.startDiscovery()
@app.route("/")
def home():
    return render_template("index.html", peers=peerManag.devices, title=db.config()["name"], name=db.config()["name"], adapters=networkManager.get_interfaces())

@app.route("/open/")
def open():
    manager.openURL("https://docs.google.com/presentation/d/1BlpnIVpDFSrweIgXjYzX46dmdsnnJIAJDOUVnizpIg0/pub?start=true&loop=true&delayms=3000")
    time.sleep(1)
    manager.getScreenShot()
    return "Done"

@app.route("/restart/")
def restart():
    call("sudo shutdown -h now", shell=True)
    
@app.route("/idle/")
def idleScreen():
    return render_template("idle.html", name=db.config()["name"], url=db.config()["url"])
    
    
@app.route("/getScreenshot/")
def screenshot():
    manager.getScreenShot()
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
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == "__main__":
    scheduler.start()
    apiBlueprint = api.APIV1(db, cecManag, manager, peerManag).get_blueprint()
    app.register_blueprint(apiBlueprint, url_prefix='/api')
    app.run(host="0.0.0.0", port=sys.argv[2], debug=False)
    scheduler.stop()
