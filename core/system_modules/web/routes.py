"""
Web Module Routes

Part of WebDisplay
System Web Module

License: MIT license

Author: C2311231

Notes:
"""

from flask import Blueprint, render_template

bp = Blueprint("web_v2", __name__)

@bp.route("/")
def home():
    return render_template("/dashboard.html")

@bp.route("/devices")
def devices():
    return render_template("/devices.html")

@bp.route("/events")
def events():
    return render_template("/events.html")

@bp.route("/event-edit")
def event_edit():
    return render_template("/event_edit.html")

@bp.route("/groups")
def groups():
    return render_template("/groups.html")

@bp.route("/global_monitoring")
def global_monitoring():
    return render_template("/global_monitoring.html")

@bp.route("/global_settings")
def global_settings():
    return render_template("/global_settings.html")

@bp.route("/device_settings")
def device_settings():
    return render_template("/device_settings.html")

@bp.route("/device_monitoring")
def device_monitoring():
    return render_template("/device_monitoring.html")

@bp.route("/logs")
def logs():
    return render_template("/logs.html")

def get_blueprint():
    return bp