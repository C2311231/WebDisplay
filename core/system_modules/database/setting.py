from core.system_modules.database.extentions import db

class Setting(db.Model):
    __tablename__ = "setting"
    id = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String(100), nullable=False)
    default_value = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    def __init__(self, setting_name: str, default_value: str, type: str, description: str, validation_data: dict, user_facing: bool):
        self.setting_name = setting_name
        self.default_value = default_value
        self.type = type
        self.description = description
        self.validation_data = validation_data
        self.user_facing = user_facing
        
        # TODO load this from the config database
        self.value = default_value