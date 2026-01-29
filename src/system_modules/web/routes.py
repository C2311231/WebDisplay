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
    return render_template("/layout.html")

def get_blueprint():
    return bp