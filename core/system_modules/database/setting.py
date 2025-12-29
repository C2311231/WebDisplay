class Setting:
    def __init__(self, setting_name: str, default_value: str, type: str, description: str, validation_data: dict, user_facing: bool):
        self.setting_name = setting_name
        self.default_value = default_value
        self.type = type
        self.description = description
        self.validation_data = validation_data
        self.user_facing = user_facing
        
        # TODO load this from the config database
        self.value = default_value