"""
Common Classes and Functions

Part of WebDisplay
System

License: MIT license

Author: C2311231

Notes:
- Actively being phased out
"""
import json


class BaseClass:
    def tick(self) -> None:
        # Run any maintenance tasks and checks (about every 5 seconds)
        pass

    def required_config(self) -> dict:
        # Required configuration data in database in format {parameter: default} (None results in defaulting to parameters set by other classes, if none are set an error will be thrown)
        return {}

    def api_endpoints(self) -> list[dict]:
        # API endpoints in format [{"endpoint_type": "endpoint_type", "function": function, "endpoint_domain": "domain", "endpoint_name": "name"}] (function must return a response object)
        return []


class Address:
    def __init__(self, address: str):
        split_address = address.strip().split(".")

        # Data Validation
        if len(split_address) != 4:
            raise ValueError()

        for value in split_address:

            if not value.isdigit():
                raise ValueError()

            elif len(value) > 3:
                raise ValueError()

            elif int(value) < 0 or int(value) > 255:
                raise ValueError()

        self.address = [int(value) for value in split_address]

    def is_multicast(self) -> bool:
        if self.address[0] >= 224 and self.address[0] <= 239:
            return True
        return False

    def __str__(self) -> str:
        return (
            f"{self.address[0]}.{self.address[1]}.{self.address[2]}.{self.address[3]}"
        )


class Url:
    def __init__(self, url: str):
        self.url = url

    def __str__(self) -> str:
        return self.url


class Response:
    def __init__(self, error, status: str, message: str, code: int, data: dict):
        self.status = status
        self.error = error
        self.message = message
        self.data = data
        self.code = code

    def to_json(self) -> str:
        return json.dumps(
            {
                "status": self.status,
                "error": self.error,
                "message": self.message,
                "code": self.code,
                "data": self.data,
            }
        )
