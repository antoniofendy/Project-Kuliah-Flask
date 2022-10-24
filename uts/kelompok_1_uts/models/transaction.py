from datetime import datetime, timedelta
from kelompok_1_uts import db
import enum


class TransactionStatus(enum.Enum):
    UNPAID = "Belum Dibayar"
    RENT = "Disewa"
    RETURNED = "Selesai"


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey("stock.id"), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey("member.id"), nullable=False)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False)
    charge_id = db.Column(db.Integer, db.ForeignKey("charge_rule.id"), nullable=False)

    rental_start_date = db.Column(db.Date, nullable=False)
    rental_end_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, default=None)

    created_at = db.Column(
        db.DateTime, nullable=False, default=(datetime.utcnow() + timedelta(hours=7))
    )
    updated_at = db.Column(
        db.DateTime,
        default=(datetime.utcnow() + timedelta(hours=7)),
        onupdate=(datetime.utcnow() + timedelta(hours=7)),
    )
    status = db.Column(
        db.Enum(TransactionStatus), nullable=False, default=TransactionStatus.UNPAID
    )

    payment = db.relationship("Payment", backref="transaction", lazy=True)
