"""
Web Module Manager

Part of WebDisplay
System Web Module

License: MIT license

Author: C2311231

Notes:
"""

import core.system as system
import core.module as module_base
from flask import Flask, request
import core.system_modules.web.routes as routes
import threading
import os
import core.system_modules.api.api_registry as api_registry
import core.system_modules.database.database as database_module

base_dir = os.path.dirname(__file__)

class web_module(module_base.module):
    def __init__(self, system: system.system):
        self.system = system
        system.require_modules("api_registry")
                                       
    def start(self) -> None:
        self.app = Flask(__name__, template_folder=os.path.join(base_dir, "templates"), static_folder=os.path.join(base_dir, "static"))
        self.api: api_registry.ApiRegistry = self.system.get_module("api_registry")  # type: ignore
        self.app = Flask(__name__, template_folder=os.path.join(base_dir, "templates"), static_folder=os.path.join(base_dir, "static"))
        self.register_routes()
        self.run_app()
        
    def register_routes(self) -> None:
        @self.app.after_request
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
        @self.app.route("/api/", methods=["POST"])
        def api_http_endpoint(self):
            """
            API HTTP endpoint for processing requests.
            (Just for reference, not finished implementing yet)
            """
            api_response = self.api.process_request(request.data.decode("utf-8"))
            return api_response.to_json(), api_response.code # type: ignore

        bp = routes.get_blueprint()
        self.app.register_blueprint(bp, url_prefix="/")
        
    def get_flask_app(self) -> Flask:
        return self.app
    
    def run_app(self, host: str = "0.0.0.0", port: int = 5000) -> None:
        threading.Thread(target=self._threaded_run, args=(host, port), daemon=True).start()
        
    def _threaded_run(self, host: str = "0.0.0.0", port: int = 5000) -> None:
        self.app.run(host=host, port=port)
        
def register(system: system.system) -> tuple[str, module_base.module]:
    module_id = "web_app"
    return module_id, web_module(system)