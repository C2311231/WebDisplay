from flask import Blueprint, render_template

bp = Blueprint("web_v2", __name__)

@bp.route("/")
def home():
    return render_template("/WebInterfaceV2/dashboard.html")

@bp.route("/devices")
def devices():
    return render_template("/WebInterfaceV2/devices.html")

@bp.route("/events")
def events():
    return render_template("/WebInterfaceV2/events.html")

@bp.route("/event-edit")
def event_edit():
    return render_template("/WebInterfaceV2/event_edit.html")

@bp.route("/groups")
def groups():
    return render_template("/WebInterfaceV2/groups.html")

@bp.route("/global_monitoring")
def global_monitoring():
    return render_template("/WebInterfaceV2/global_monitoring.html")

@bp.route("/global_settings")
def global_settings():
    return render_template("/WebInterfaceV2/global_settings.html")

@bp.route("/device_settings")
def device_settings():
    return render_template("/WebInterfaceV2/device_settings.html")

@bp.route("/device_monitoring")
def device_monitoring():
    return render_template("/WebInterfaceV2/device_monitoring.html")

@bp.route("/logs")
def logs():
    return render_template("/WebInterfaceV2/logs.html")

def get_blueprint():
    return bp