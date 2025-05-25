import commons
import json
import database

class APIv2(commons.BaseClass):

    def __init__(self, db: database.Database) -> None:
        self.endpoints = []
        self.db = db
        self.add_endpoints(self.api_endpoints())

    def add_endpoints(self, endpoints: list[dict]) -> None:
        for endpoint in endpoints:
            self.endpoints.append(endpoint)

    def process_request(self, request: str) -> commons.Response:
        # Process the request here
        # Example structure of request:
        # {
        #     "id": "request_id", (optional)
        #     "type": "x", (trigger, get, post, inform, acknowledge)
        #     "version": "v2", (only v2 is currently supported)
        #     "destination": "destination_id",
        #     "domain": "endpoint_domain",
        #     "name": "endpoint_name",
        #     "data": {}
        # }

        try:
            request = json.loads(request)
        except json.JSONDecodeError:
            return commons.Response(True, "error", "Invalid JSON format", 400, "")

        # Validate the request structure
        if not isinstance(request, dict):
            return commons.Response(True, "error", "Invalid request format", 400, "")

        if (
            "type" not in request
            or "version" not in request
            or "name" not in request
            or "domain" not in request
            or "destination" not in request
            or "data" not in request
        ):
            return commons.Response(True, "error", "Missing required fields", 400, "")

        if request["version"] != "v2":  # type: ignore
            return commons.Response(True, "error", "Unrecognized version", 400, "")

        if request["type"] not in ["trigger", "get", "post", "inform", "acknowledge"]:  # type: ignore
            return commons.Response(True, "error", "Unrecognized command type", 400, "")
        
        if not isinstance(request["data"], dict):  # type: ignore
            return commons.Response(True, "error", "Invalid data format", 400, "")

        if request["destination"] != self.db.config()["device_id"] and request["destination"] not in json.loads(self.db.config()["group_ids"]):  # type: ignore
            return commons.Response(True, "error", "Unintended destination", 0, "")

        for endpoint in self.endpoints:
            if (
                endpoint["endpoint_domain"] == request["domain"]  # type: ignore
                and endpoint["endpoint_name"] == request["name"]  # type: ignore
                and endpoint["endpoint_type"] == request["type"]  # type: ignore
            ):
                # Call the function associated with the endpoint
                response = endpoint(**request["data"]) # type: ignore
                if isinstance(response, commons.Response):
                    return response
                else:
                    return commons.Response(
                        True, "error", "Invalid function response format", 500, ""
                    )
        return commons.Response(True, "error", "Invalid endpoint", 400, "")
    
    def required_config(self) -> dict:
        return {
            "device_id": None,
            "group_ids": [0],
        }