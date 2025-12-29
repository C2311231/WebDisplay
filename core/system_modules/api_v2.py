import commons, database
import json
import requests

class APIv2(commons.BaseClass):

    def __init__(self, local_config: dict) -> None:
        self.endpoints = []
        self.config = local_config
        self.add_endpoints(self.api_endpoints())

    def add_endpoints(self, endpoints: list[dict]) -> None:
        for endpoint in endpoints:
            self.endpoints.append(endpoint)

    def process_request(self, request: str) -> commons.Response:
        # Process the request here
        # Example structure of request:
        # {
        #     "id": "request_id", (optional)
        #     "type": "x", (trigger, get, post, inform, delete)
        #     "version": "v2", (only v2 is currently supported)
        #     "destination": "destination_id",
        #     "source": "source_id",
        #     "domain": "endpoint_domain",
        #     "name": "endpoint_name",
        #     "data": {}
        # }
        id = -1
        # Check if the request is a valid JSON string
        
        try:
            request = json.loads(request.strip())
        except json.JSONDecodeError:
            return commons.Response(True, "error", "Invalid JSON format", 400, {"id": id})

        # Validate the request structure
        if not isinstance(request, dict):
            return commons.Response(True, "error", "Invalid request format", 400, {"id": id})

        if "id" in request:
            if not isinstance(request["id"], int):  # type: ignore
                return commons.Response(True, "error", "Invalid request ID format", 400, {"id": id})
            id = request["id"]  # type: ignore

        if (
            "type" not in request
            or "version" not in request
            or "name" not in request
            or "domain" not in request
            or "destination" not in request
            or "data" not in request
            or "source" not in request
        ):
            return commons.Response(True, "error", "Missing required fields", 400, {"id": id})

        if request["version"] != "v2":  # type: ignore
            return commons.Response(True, "error", "Unrecognized version", 400, {"id": id})

        if request["type"] not in ["trigger", "get", "post", "delete", "inform"]:  # type: ignore
            return commons.Response(True, "error", "Unrecognized command type", 400, {"id": id})

        if not isinstance(request["data"], dict):  # type: ignore
            return commons.Response(True, "error", "Invalid data format", 400, {"id": id})

        if request["destination"] != self.config["device_id"] and request["destination"] not in json.loads(self.config["group_ids"]) and request["destination"] != "0":  # type: ignore
            return commons.Response(True, "error", "Unintended destination", 0, {"id": id})

        for endpoint in self.endpoints:
            if (
                endpoint["endpoint_domain"] == request["domain"]  # type: ignore
                and endpoint["endpoint_name"] == request["name"]  # type: ignore
                and endpoint["endpoint_type"] == request["type"]  # type: ignore
            ):
                # Call the function associated with the endpoint
                response = endpoint["function"](**request["data"])  # type: ignore
                
                # Check if the response is a valid Response object
                if isinstance(response, commons.Response):
                    response.data["id"] = id
                    return response
                else:
                    return commons.Response(
                        True, "error", "Invalid function response format", 500, {"id": id}
                    )
        return commons.Response(True, "error", "Invalid endpoint", 400, {"id": id})

    def noOp(self) -> commons.Response:
        return commons.Response(False, "success", "No operation performed", 200, {})

    def api_endpoints(self) -> list[dict]:
        return [
            {
                "endpoint_type": "trigger",
                "function": self.noOp,
                "endpoint_domain": "api",
                "endpoint_name": "noOp",
            },
        ]

    def required_config(self) -> dict:
        return {
            "device_id": None,
            "group_ids": json.dumps([0]),
        }


def call_http_api(local_id: str, ip:str, port:int, device_id:str, endpoint_type: str, endpoint_domain:str, endpoint_name:str, data:dict) -> commons.Response:
    """
    Calls an HTTP API endpoint on a device.
    
    :param ip: The IP address of the device.
    :param port: The port number of the device's API.
    :param device_id: The ID of the device.
    :param endpoint_domain: The domain of the API endpoint.
    :param endpoint_name: The name of the API endpoint.
    :param data: The data to send to the API endpoint.
    :return: A Response object containing the result of the API call.
    """
    response = requests.post(
        f"http://{ip}:{port}/api",
        json={
            "type": endpoint_type,
            "version": "v2",
            "destination": device_id,
            "source": local_id,
            "domain": endpoint_domain,
            "name": endpoint_name,
            "data": data
        }
    )
    
    if response.ok and response.json().get("code") == 200:
        return commons.Response(False, "success", "API call successful", 200, response.json().get("data", {}))
    else:
        return commons.Response(True, "error", f"API call failed: {response.text}", response.status_code, {})
