"""
API response class

Part of WebDisplay
System API Module

License: MIT license

Author: C2311231

Notes:
"""

class APIResponse:
    def __init__(self, status: str, data: dict | None = None, error: str | None = None):
        self.status = status
        self.data = data or {}
        self.error = error

    def to_json(self):
        return {"status": self.status, "data": self.data, "error": self.error}