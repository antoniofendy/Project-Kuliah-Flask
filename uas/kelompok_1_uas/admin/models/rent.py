from kelompok_1_uas import db

import enum


class PaymentType(enum.Enum):
    PAYMENT = "Pembayaran"
    CHARGE = "Denda"


class RentStatus(enum.Enum):
    UNPAID = "Belum dibayar"
    PENDING = "Menunggu Konfirmasi"
    PAID = "Dibayar"


class Rent(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    reservation_id = db.Column(db.Integer, db.ForeignKey("reservation.id"))
    charge_rule_id = db.Column(db.Integer, db.ForeignKey("charge_rule.id"))
    type = db.Column(db.Enum(PaymentType))
    transfer_file = db.Column(db.String(255))
    total = db.Column(db.Integer)
    status = db.Column(db.Enum(RentStatus))

    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    user = db.relationship("User", backref="rent_user", lazy=True)
    admin = db.relationship("Admin", backref="rent_admin", lazy=True)
    stock = db.relationship("Stock", backref="rent_stock", lazy=True)
    reservation = db.relationship("Reservation", backref="rent_reservation", lazy=True)
    charge_rule = db.relationship("ChargeRule", backref="rent_charge_rule", lazy=True)
