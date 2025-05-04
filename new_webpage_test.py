from flask import render_template, redirect, Flask
app = Flask(__name__)
@app.route("/")
def home():
    return render_template("/WebInterfaceV2/dashboard.html")

@app.route("/devices")
def devices():
    return render_template("/WebInterfaceV2/devices.html")

@app.route("/events")
def events():
    return render_template("/WebInterfaceV2/events.html")

@app.route("/groups")
def groups():
    return render_template("/WebInterfaceV2/groups.html")

@app.route("/global_monitoring")
def global_monitoring():
    return render_template("/WebInterfaceV2/global_monitoring.html")

@app.route("/global_settings")
def global_settings():
    return render_template("/WebInterfaceV2/global_settings.html")

@app.route("/device_settings")
def device_settings():
    return render_template("/WebInterfaceV2/device_settings.html")

@app.route("/device_monitoring")
def device_monitoring():
    return render_template("/WebInterfaceV2/device_monitoring.html")

@app.route("/logs")
def logs():
    return render_template("/WebInterfaceV2/logs.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)