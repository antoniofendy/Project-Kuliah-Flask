from kelompok_1_uas import db
from flask_login import UserMixin


class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(16))
    address = db.Column(db.String(255))
    email = db.Column(db.String(140), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
