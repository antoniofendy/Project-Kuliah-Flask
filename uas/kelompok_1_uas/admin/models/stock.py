from kelompok_1_uas import db


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey("car.id"), nullable=False)
    garage_id = db.Column(db.Integer, db.ForeignKey("garage.id"), nullable=False)
    price_per_day = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    car = db.relationship("Car", backref="stock", lazy=True)
    garage = db.relationship("Garage", backref="stock", lazy=True)

    # def __repr__(self) -> str:
    #     return f"<Stock {self.id}:Car {self.car_id}>"
