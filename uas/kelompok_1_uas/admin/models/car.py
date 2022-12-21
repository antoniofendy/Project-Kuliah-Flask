from kelompok_1_uas import db

import enum

class Transmission(enum.Enum):
    manual = "Manual"
    automatic = "Automatic"

class Fuel(enum.Enum):
    petrol = "Petrol"
    electric = "Electric"

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    brand = db.Column(db.String(255), nullable=False)
    picture = db.Column(db.String(255), nullable=False)
    transmission = db.Column(db.Enum(Transmission), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    luggage = db.Column(db.Integer, nullable=False)
    fuel = db.Column(db.Enum(Fuel), nullable=False)

    # stock = db.relationship("Stock", backref="car_has_stock", lazy=True)
