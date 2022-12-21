from kelompok_1_uas import db

import enum

class ReservationStatus(enum.Enum):
    OPEN = "Menunggu Konfirmasi"
    RENTED = "Disewa"
    RETURN = "Dikembalikan"
    FAIL = "Gagal"

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    pickup_garage_id = db.Column(db.Integer, db.ForeignKey("garage.id"), nullable=False)
    dropoff_garage_id = db.Column(db.Integer, db.ForeignKey("garage.id"), nullable=False)

    pickup_datetime = db.Column(db.DateTime)
    dropoff_datetime = db.Column(db.DateTime)
    note = db.Column(db.Text)
    status = db.Column(db.Enum(ReservationStatus))

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    user = db.relationship("User", backref="reservation_user", lazy=True)
    stock = db.relationship("Stock", backref="reservation_stock", lazy=True)
    pickup = db.relationship("Garage", backref="reservation_pickup", lazy=True, foreign_keys=pickup_garage_id)
    dropoff = db.relationship("Garage", backref="reservation_dropoff", lazy=True, foreign_keys=dropoff_garage_id)
