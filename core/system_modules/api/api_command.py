class APICommand():
     def __init__(self, capability: str, capability_version: int, name: str, handler, description: str, example: str):
        self.capability = capability
        self.capability_version = capability_version
        self.name = name
        self.handler = handler
        self.description = description
        self.example = example

     def get_callback(self):
        return self.handler