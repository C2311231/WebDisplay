from core.system_modules.database.extentions import db

class dbSetting(db.Model):
    __tablename__ = "setting"
    id = db.Column(db.Integer, primary_key=True)
    setting_name = db.Column(db.String(100), nullable=False)
    domain = db.Column(db.String(300), nullable=False)
    value = db.Column(db.String(255), nullable=False)
    version = db.Column(db.String(5), nullable=False)